from pathlib import Path
import pandas as pd
import re

DATA_DIR = Path("data")
REPORT_DIR = Path("reports")

REPORT_DIR.mkdir(exist_ok=True)

EXPECTED_COLUMNS = [
    "MDDS STC",
    "STATE NAME",
    "MDDS DTC",
    "DISTRICT NAME",
    "MDDS Sub_DT",
    "SUB-DISTRICT NAME",
    "MDDS PLCN",
    "Area Name"
]


def read_dataset(file_path):
    suffix = file_path.suffix.lower()

    if suffix == ".xls":
        engine = "xlrd"

    elif suffix == ".ods":
        engine = "odf"

    elif suffix == ".xlsx":
        engine = "openpyxl"

    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    # ------------------------------------------------
    # Read all sheets
    # ------------------------------------------------

    excel_file = pd.ExcelFile(
        file_path,
        engine=engine
    )

    # ------------------------------------------------
    # Find the sheet containing the expected columns
    # ------------------------------------------------

    for sheet_name in excel_file.sheet_names:

        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            dtype=str,
            engine=engine
        )

        # Clean column names
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # Check whether this is the Village Directory sheet
        if all(
            column in df.columns
            for column in EXPECTED_COLUMNS
        ):
            print(
                f"  Using sheet: {sheet_name}"
            )

            return df

    # ------------------------------------------------
    # No valid sheet found
    # ------------------------------------------------

    raise ValueError(
        f"No sheet containing all expected columns found. "
        f"Available sheets: {excel_file.sheet_names}"
    )
def clean_dataframe(df):
    # Convert everything to strings
    df = df.astype("string")

    # Remove surrounding spaces
    for column in df.columns:
        df[column] = df[column].str.strip()

    return df


def check_columns(df):
    actual = list(df.columns)

    missing = [
        column for column in EXPECTED_COLUMNS
        if column not in actual
    ]

    extra = [
        column for column in actual
        if column not in EXPECTED_COLUMNS
    ]

    return missing, extra


def check_code_format(series, expected_length):
    """
    Checks whether non-null codes contain exactly
    the expected number of digits.
    """

    values = series.dropna().astype(str).str.strip()

    invalid = values[
        ~values.str.fullmatch(rf"\d{{{expected_length}}}")
    ]

    return invalid


def validate_standard_dataset(file_path):

    result = {
        "file": file_path.name,
        "status": "PASS",
        "rows": 0,
        "missing_values": 0,
        "duplicate_rows": 0,
        "invalid_state_codes": 0,
        "invalid_district_codes": 0,
        "invalid_subdistrict_codes": 0,
        "invalid_village_codes": 0,
        "hierarchy_errors": 0,
        "notes": ""
    }

    try:
        df = read_dataset(file_path)
        df = clean_dataframe(df)

        result["rows"] = len(df)

        # ------------------------------------------------
        # 1. Column validation
        # ------------------------------------------------

        missing_columns, extra_columns = check_columns(df)

        if missing_columns:
            result["status"] = "REVIEW"
            result["notes"] += (
                f"Missing columns: {missing_columns}. "
            )

            return result

        # ------------------------------------------------
        # 2. Missing values
        # ------------------------------------------------

        missing_mask = (
            df[EXPECTED_COLUMNS]
          .isna()
          | df[EXPECTED_COLUMNS].apply(
                lambda col: col.astype("string").str.strip().eq("")
         )
        )

        missing_count = int(missing_mask.sum().sum())

        result["missing_values"] = missing_count

        if missing_count > 0:
            result["status"] = "REVIEW"

        # ------------------------------------------------
        # 3. Duplicate rows
        # ------------------------------------------------

        duplicate_count = int(
            df[EXPECTED_COLUMNS].duplicated().sum()
        )

        result["duplicate_rows"] = duplicate_count

        if duplicate_count > 0:
            result["status"] = "REVIEW"

        # ------------------------------------------------
        # 4. State code
        # ------------------------------------------------

        invalid_state = check_code_format(
            df["MDDS STC"],
            2
        )

        result["invalid_state_codes"] = len(invalid_state)

        # ------------------------------------------------
        # 5. District code
        # ------------------------------------------------

        invalid_district = check_code_format(
            df["MDDS DTC"],
            3
        )

        result["invalid_district_codes"] = len(invalid_district)

        # ------------------------------------------------
        # 6. Sub-district code
        # ------------------------------------------------

        invalid_subdistrict = check_code_format(
            df["MDDS Sub_DT"],
            5
        )

        result["invalid_subdistrict_codes"] = len(
            invalid_subdistrict
        )

        # ------------------------------------------------
        # 7. Village/locality code
        # ------------------------------------------------

        invalid_village = check_code_format(
            df["MDDS PLCN"],
            6
        )

        result["invalid_village_codes"] = len(
            invalid_village
        )

        # ------------------------------------------------
        # 8. Hierarchy validation
        # ------------------------------------------------

        hierarchy_errors = 0

        # Every row should belong to exactly one state
        state_count = df["MDDS STC"].nunique()

        if state_count != 1:
            hierarchy_errors += 1

        # Check state name consistency
        state_names = df["STATE NAME"].dropna().unique()

        if len(state_names) != 1:
            hierarchy_errors += 1

        result["hierarchy_errors"] = hierarchy_errors

        # ------------------------------------------------
        # Final status
        # ------------------------------------------------

        if (
            result["invalid_state_codes"] > 0
            or result["invalid_district_codes"] > 0
            or result["invalid_subdistrict_codes"] > 0
            or result["invalid_village_codes"] > 0
            or result["hierarchy_errors"] > 0
        ):
            result["status"] = "REVIEW"

        if extra_columns:
            result["notes"] += (
                f"Extra columns: {extra_columns}. "
            )

    except Exception as error:

        result["status"] = "ERROR"
        result["notes"] = str(error)

    return result


def main():

    files = sorted([
        file
        for file in DATA_DIR.iterdir()
        if file.suffix.lower() in [".xls", ".ods", ".xlsx"]
    ])

    print("=" * 80)
    print("MDDS DATASET VALIDATION")
    print("=" * 80)

    print(f"Files found: {len(files)}")

    results = []

    for file_path in files:

        print(f"\nValidating: {file_path.name}")

        result = validate_standard_dataset(file_path)

        results.append(result)

        print(f"Status: {result['status']}")
        print(f"Rows: {result['rows']:,}")
        print(f"Missing values: {result['missing_values']:,}")
        print(f"Duplicate rows: {result['duplicate_rows']:,}")

        if result["notes"]:
            print(f"Notes: {result['notes']}")

    # ------------------------------------------------
    # Save report
    # ------------------------------------------------

    report_df = pd.DataFrame(results)

    report_path = REPORT_DIR / "validation_summary.csv"

    report_df.to_csv(
        report_path,
        index=False
    )

    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)

    print(f"\nReport saved to:")
    print(report_path)

    print("\nStatus summary:")

    print(
        report_df["status"]
        .value_counts()
        .to_string()
    )


if __name__ == "__main__":
    main()