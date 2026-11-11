"""Build the 2025 GEIH household and person datasets from the original DANE archives."""

import argparse
from contextlib import ExitStack
import fnmatch
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
YEAR = 2025
MONTH_NAMES = (
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
    "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
)
HOUSEHOLD_KEY = ["PER", "MES", "DIRECTORIO", "SECUENCIA_P", "HOGAR"]
PERSON_KEY = HOUSEHOLD_KEY + ["ORDEN"]
POVERTY_KEY = ["directorio", "secuencia_p", "link_month"]
HEAD_FIELDS = ["ORDEN", "P6050", "P6040", "P3042", "P3271", "P3039"]
HOUSING_FIELDS = ["AREA", "P6008", "P5090", "P5100", "P5130", "P5140", "FEX_C18"]
OUTPUT_NAME = "geih_households_2025.parquet"
LINKED_OUTPUT_NAME = "geih_poverty_households_2025.parquet"
PERSON_OUTPUT_NAME = "geih_persons_housing_2025.parquet"
MANIFEST_NAME = "geih_households_2025_manifest.json"


def fingerprint(path):
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256")
    return {"file": path.name, "bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def read_module(archive, pattern):
    # The December housing member contains non-breaking spaces in its name.
    members = [
        name for name in archive.namelist()
        if fnmatch.fnmatchcase(name.replace("\u00a0", " "), pattern)
    ]
    if len(members) != 1:
        raise ValueError(f"{archive.filename}: expected one member for {pattern!r}, got {members}")
    with archive.open(members[0]) as stream:
        return pd.read_csv(stream, sep=";", encoding="latin-1", dtype="string")


def validate_key(frame, key, label):
    for field in key:
        frame[field] = frame[field].str.strip()
    if frame[key].isna().any().any() or frame[key].eq("").any().any():
        raise ValueError(f"{label}: incomplete identifiers")
    if frame.duplicated(key).any():
        raise ValueError(f"{label}: duplicate identifiers for {key}")


def build_month(path, month, sources):
    with ZipFile(path) as archive:
        housing = read_module(archive, sources["geih_housing_member_pattern"])
        people = read_module(archive, sources["geih_person_member_pattern"])

    missing = set(HOUSEHOLD_KEY + HOUSING_FIELDS) - set(housing)
    if missing:
        raise ValueError(f"{path.name}: missing housing columns {sorted(missing)}")
    for label, frame, key in (
        ("housing", housing, HOUSEHOLD_KEY),
        ("persons", people, PERSON_KEY),
    ):
        validate_key(frame, key, f"{path.name} {label}")
        if not frame["PER"].eq(str(YEAR)).all() or not pd.to_numeric(frame["MES"]).eq(month).all():
            raise ValueError(f"{path.name}: inconsistent year or month in {label}")

    heads = people.loc[people["P6050"].eq("1"), HOUSEHOLD_KEY + HEAD_FIELDS].copy()
    validate_key(heads, HOUSEHOLD_KEY, f"{path.name} heads")
    residents = people.groupby(HOUSEHOLD_KEY, sort=False).size().rename("resident_count")
    head_profile = heads.merge(residents, on=HOUSEHOLD_KEY, how="outer", validate="one_to_one", indicator=True)
    if not head_profile["_merge"].eq("both").all():
        raise ValueError(f"{path.name}: a household lacks a head or a resident count")

    for field in ("P6008", "P5090"):
        housing[field] = pd.to_numeric(housing[field], errors="raise").astype("Int64")
    for field in ("P5100", "P5130", "P5140", "FEX_C18"):
        housing[field] = pd.to_numeric(housing[field], errors="raise").astype("Float64")
    for field in HEAD_FIELDS:
        head_profile[field] = pd.to_numeric(head_profile[field], errors="raise").astype("Int64")
        people[field] = pd.to_numeric(people[field], errors="raise").astype("Int64")
    people["FEX_C18"] = pd.to_numeric(people["FEX_C18"], errors="raise").astype("Float64")

    master = housing.merge(
        head_profile.drop(columns="_merge"),
        on=HOUSEHOLD_KEY, how="outer", validate="one_to_one", indicator=True,
    )
    if not master["_merge"].eq("both").all() or len(master) != len(housing):
        raise ValueError(f"{path.name}: household coverage differs between GEIH modules")
    master = master.drop(columns="_merge")
    if master["P6008"].isna().any() or not master["P6008"].eq(master["resident_count"]).all():
        raise ValueError(f"{path.name}: P6008 disagrees with the number of person records")

    # Keep shared identifiers once. Preserve both values of other shared fields.
    person_aliases = {
        field: f"person_{field.lower()}"
        for field in people.columns if field in housing.columns and field not in HOUSEHOLD_KEY
    }
    person_master = people.rename(columns=person_aliases).merge(
        housing, on=HOUSEHOLD_KEY, how="left", validate="many_to_one", indicator=True,
    )
    if len(person_master) != len(people) or not person_master["_merge"].eq("both").all():
        raise ValueError(f"{path.name}: some person records could not link to housing")
    person_master = person_master.drop(columns="_merge")

    coverage = {
        "month": month,
        "household_months": len(master),
        "cali_household_months": int(master["AREA"].eq("76").sum()),
        "person_rows_checked": len(person_master),
        "cali_person_months": int(person_master["AREA"].eq("76").sum()),
    }
    return master, person_master, coverage, person_aliases


def link_poverty(master, archive_path, member):
    with ZipFile(archive_path) as archive, archive.open(member) as stream:
        poverty = pd.read_csv(stream, encoding="utf-8-sig", dtype="string")
    for field in ("nper", "npersug", "clase", "p5090", "pobre", "indigente", "npobres", "nindigentes"):
        poverty[field] = pd.to_numeric(poverty[field], errors="raise").astype("Int64")
    for field in ("ingtotug", "lp", "li", "p5100", "p5130", "ingtotarr", "ingpcug", "fex_c", "fex_dpto"):
        poverty[field] = pd.to_numeric(poverty[field], errors="raise").astype("Float64")

    # GEIH uses months such as "01"; poverty uses "1". Normalize only the join copies.
    poverty["link_month"] = pd.to_numeric(poverty["mes"]).astype("Int64").astype("string")
    housing = master[["DIRECTORIO", "SECUENCIA_P"]].rename(
        columns={"DIRECTORIO": "directorio", "SECUENCIA_P": "secuencia_p"},
    )
    housing["link_month"] = pd.to_numeric(master["MES"]).astype("Int64").astype("string")
    validate_key(poverty, POVERTY_KEY, archive_path.name)
    validate_key(housing, POVERTY_KEY, "GEIH shared poverty key")
    payload = poverty.drop(columns="mes")
    master_names = {field.lower() for field in master.columns}
    poverty_aliases = {
        field: f"poverty_{field}"
        for field in payload.columns if field not in POVERTY_KEY and field.lower() in master_names
    }
    linked = pd.concat([master, housing], axis=1).merge(
        payload.rename(columns=poverty_aliases), on=POVERTY_KEY,
        how="left", validate="one_to_one", indicator="poverty_match_status",
    )
    linked = linked.drop(columns=POVERTY_KEY)
    if not linked[HOUSEHOLD_KEY].equals(master[HOUSEHOLD_KEY]):
        raise ValueError("Poverty left join changed the GEIH household rows")
    is_matched = linked["poverty_match_status"].eq("both")
    matched = linked.loc[is_matched]
    if matched["nper"].isna().any() or not matched["nper"].eq(matched["resident_count"]).all():
        raise ValueError("Poverty nper disagrees with GEIH resident counts on linked rows")
    tenure = matched[poverty_aliases["p5090"]]
    if tenure.isna().any() or not tenure.eq(matched["P5090"]).all():
        raise ValueError("Poverty p5090 disagrees with GEIH tenure on linked rows")
    if not matched["AREA"].eq("76").fillna(False).eq(matched["dominio"].eq("CALI").fillna(False)).all():
        raise ValueError("Cali domain differs between the linked sources")
    for field in ("ingtotug", "fex_c"):
        if matched[field].isna().any():
            raise ValueError(f"Poverty {field} is missing on linked rows")

    linked["poverty_match_status"] = is_matched.map({True: "matched", False: "unmatched"})
    coverage = {
        "member": member,
        "household_rows": len(poverty),
        "matched_geih_households": len(matched),
        "geih_without_poverty_match": int((~is_matched).sum()),
        "poverty_without_geih_match": len(poverty) - len(matched),
        "cali_matched_households": int(matched["AREA"].eq("76").sum()),
        "aliased_columns": poverty_aliases,
    }
    return linked, coverage


def build_annual_geih(archives, sources, person_path):
    frames, monthly = [], []
    with ExitStack() as stack:
        writer = None
        for month, name in enumerate(MONTH_NAMES, 1):
            path = archives / f"{name} {YEAR}.zip"
            frame, person_master, coverage, aliases = build_month(path, month, sources)
            person_table = pa.Table.from_pandas(person_master, preserve_index=False)
            if writer is None:
                writer = stack.enter_context(pq.ParquetWriter(person_path, person_table.schema, compression="zstd"))
            writer.write_table(person_table)
            frames.append(frame)
            monthly.append({**coverage, **fingerprint(path)})
            print(f"{name}: {len(frame):,} household-months; {len(person_master):,} person-months", flush=True)
    return pd.concat(frames, ignore_index=True), monthly, aliases


def write_households(frame, path):
    frame.to_parquet(path, index=False, engine="pyarrow", compression="zstd")
    saved_keys = pd.read_parquet(path, columns=HOUSEHOLD_KEY)
    if not saved_keys.equals(frame[HOUSEHOLD_KEY]):
        raise ValueError(f"{path.name}: Parquet round trip changed the household keys")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, help="Optional source configuration path")
    args = parser.parse_args()
    config = args.config or ROOT / "config/data_sources.json"
    sources = json.loads(config.read_text(encoding="utf-8-sig"))
    archives = ROOT / sources["geih_archive_directory"]
    poverty_archive = ROOT / sources["poverty_archive_path"]

    output_dir = ROOT / "data/processed"
    manifest = ROOT / "data/reference" / MANIFEST_NAME
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output_dir) as temporary:
        candidate_dir = Path(temporary)
        person_path = candidate_dir / PERSON_OUTPUT_NAME
        master, monthly, person_aliases = build_annual_geih(archives, sources, person_path)
        validate_key(master, HOUSEHOLD_KEY, "annual GEIH")
        linked, poverty_coverage = link_poverty(master, poverty_archive, sources["poverty_household_member"])
        write_households(master, candidate_dir / OUTPUT_NAME)
        write_households(linked, candidate_dir / LINKED_OUTPUT_NAME)

        person_metadata = pq.read_metadata(person_path)
        if person_metadata.num_rows != int(master["resident_count"].sum()):
            raise ValueError("Annual person rows do not reconcile with GEIH household resident counts")
        report = {
            "survey_year": YEAR,
            "unit": "household-month",
            "household_key": HOUSEHOLD_KEY,
            "household_months": len(master),
            "cali_household_months": int(master["AREA"].eq("76").sum()),
            "columns": len(master.columns),
            "geih_output": fingerprint(candidate_dir / OUTPUT_NAME),
            "linked_household_output": {
                **fingerprint(candidate_dir / LINKED_OUTPUT_NAME),
                "unit": "household-month",
                "household_months": len(linked),
                "columns": len(linked.columns),
            },
            "geih_person_output": {
                **fingerprint(person_path),
                "unit": "person-month",
                "key": PERSON_KEY,
                "person_months": person_metadata.num_rows,
                "cali_person_months": sum(entry["cali_person_months"] for entry in monthly),
                "columns": person_metadata.num_columns,
                "aliased_columns": person_aliases,
            },
            "geih_monthly_archives": monthly,
            "poverty_archive": {**fingerprint(poverty_archive), **poverty_coverage},
        }
        for filename in (OUTPUT_NAME, LINKED_OUTPUT_NAME, PERSON_OUTPUT_NAME):
            (candidate_dir / filename).replace(output_dir / filename)
    manifest.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"GEIH: {len(master):,} household-months; Cali: {report['cali_household_months']:,}")
    print(f"Poverty: {poverty_coverage['matched_geih_households']:,} verified matches")
    print(f"GEIH persons: {report['geih_person_output']['person_months']:,} person-months")
    for filename in (LINKED_OUTPUT_NAME, PERSON_OUTPUT_NAME):
        print((output_dir / filename).relative_to(ROOT))
    print(manifest.relative_to(ROOT))


if __name__ == "__main__":
    main()
