from pathlib import Path
import os
import sys

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

BACKEND_ENV = BASE_DIR.parent / "backend" / ".env"

load_dotenv(BACKEND_ENV)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found.")
    print(f"Expected .env file at: {BACKEND_ENV}")
    sys.exit(1)


EXPECTED_COLUMNS = [
    "MDDS STC",
    "STATE NAME",
    "MDDS DTC",
    "DISTRICT NAME",
    "MDDS Sub_DT",
    "SUB-DISTRICT NAME",
    "MDDS PLCN",
    "Area Name",
]


# Number of villages sent to PostgreSQL at once
BATCH_SIZE = 5000


# ============================================================
# VALUE CLEANING
# ============================================================

def clean_value(value):
    """
    Convert pandas missing values to None
    and remove unnecessary whitespace.
    """

    if pd.isna(value):
        return None

    value = str(value).strip()

    if not value:
        return None

    if value.lower() in {"nan", "none"}:
        return None

    return value


def normalize_code(value):
    """
    Normalize MDDS codes.

    Example:
        123.0 -> 123

    Codes remain strings so leading zeros are preserved.
    """

    value = clean_value(value)

    if value is None:
        return None

    if value.endswith(".0"):
        value = value[:-2]

    return value.strip()


def normalize_name(value):
    """
    Normalize names by removing extra spaces.
    """

    value = clean_value(value)

    if value is None:
        return None

    return " ".join(value.split())


# ============================================================
# DATABASE CONNECTION
# ============================================================

def connect_database():

    print("Connecting to Neon PostgreSQL...")

    connection = psycopg2.connect(DATABASE_URL)

    connection.autocommit = False

    print("Database connection successful!")

    return connection


# ============================================================
# READ DATASET
# ============================================================

def read_dataset(file_path):

    print(f"\nReading: {file_path.name}")

    extension = file_path.suffix.lower()

    # --------------------------------------------------------
    # XLS
    # --------------------------------------------------------

    if extension == ".xls":

        df = pd.read_excel(
            file_path,
            dtype=str,
            engine="xlrd"
        )

    # --------------------------------------------------------
    # ODS
    # --------------------------------------------------------

    elif extension == ".ods":

        df = pd.read_excel(
            file_path,
            dtype=str,
            engine="odf"
        )

    else:

        raise ValueError(
            f"Unsupported file format: {file_path.suffix}"
        )

    # --------------------------------------------------------
    # Clean column names
    # --------------------------------------------------------

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    # --------------------------------------------------------
    # Check required columns
    # --------------------------------------------------------

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing columns in {file_path.name}: "
            f"{missing_columns}"
        )

    # --------------------------------------------------------
    # Keep only expected columns
    # --------------------------------------------------------

    df = df[EXPECTED_COLUMNS].copy()

    # --------------------------------------------------------
    # Normalize codes
    # --------------------------------------------------------

    for column in [
        "MDDS STC",
        "MDDS DTC",
        "MDDS Sub_DT",
        "MDDS PLCN",
    ]:

        df[column] = df[column].apply(
            normalize_code
        )

    # --------------------------------------------------------
    # Normalize names
    # --------------------------------------------------------

    for column in [
        "STATE NAME",
        "DISTRICT NAME",
        "SUB-DISTRICT NAME",
        "Area Name",
    ]:

        df[column] = df[column].apply(
            normalize_name
        )

    print(
        f"Rows loaded: {len(df):,}"
    )

    return df


# ============================================================
# STATE
# ============================================================

def get_or_create_state(
    cursor,
    state_cache,
    country_id,
    state_code,
    state_name
):

    key = (
        country_id,
        state_code
    )

    # --------------------------------------------------------
    # Check memory cache
    # --------------------------------------------------------

    if key in state_cache:

        return state_cache[key]

    # --------------------------------------------------------
    # Insert / update
    # --------------------------------------------------------

    cursor.execute(
        """
        INSERT INTO states
            (
                code,
                name,
                country_id
            )
        VALUES
            (
                %s,
                %s,
                %s
            )
        ON CONFLICT (country_id, code)
        DO UPDATE SET
            name = EXCLUDED.name
        RETURNING id
        """,
        (
            state_code,
            state_name,
            country_id,
        ),
    )

    state_id = cursor.fetchone()[0]

    state_cache[key] = state_id

    return state_id


# ============================================================
# DISTRICT
# ============================================================

def get_or_create_district(
    cursor,
    district_cache,
    state_id,
    district_code,
    district_name
):

    key = (
        state_id,
        district_code
    )

    # --------------------------------------------------------
    # Check memory cache
    # --------------------------------------------------------

    if key in district_cache:

        return district_cache[key]

    # --------------------------------------------------------
    # Insert / update
    # --------------------------------------------------------

    cursor.execute(
        """
        INSERT INTO districts
            (
                code,
                name,
                state_id
            )
        VALUES
            (
                %s,
                %s,
                %s
            )
        ON CONFLICT (state_id, code)
        DO UPDATE SET
            name = EXCLUDED.name
        RETURNING id
        """,
        (
            district_code,
            district_name,
            state_id,
        ),
    )

    district_id = cursor.fetchone()[0]

    district_cache[key] = district_id

    return district_id


# ============================================================
# SUB-DISTRICT
# ============================================================

def get_or_create_subdistrict(
    cursor,
    subdistrict_cache,
    district_id,
    subdistrict_code,
    subdistrict_name
):

    key = (
        district_id,
        subdistrict_code
    )

    # --------------------------------------------------------
    # Check memory cache
    # --------------------------------------------------------

    if key in subdistrict_cache:

        return subdistrict_cache[key]

    # --------------------------------------------------------
    # Insert / update
    # --------------------------------------------------------

    cursor.execute(
        """
        INSERT INTO sub_districts
            (
                code,
                name,
                district_id
            )
        VALUES
            (
                %s,
                %s,
                %s
            )
        ON CONFLICT (district_id, code)
        DO UPDATE SET
            name = EXCLUDED.name
        RETURNING id
        """,
        (
            subdistrict_code,
            subdistrict_name,
            district_id,
        ),
    )

    subdistrict_id = cursor.fetchone()[0]

    subdistrict_cache[key] = subdistrict_id

    return subdistrict_id


# ============================================================
# VILLAGE BATCH INSERT
# ============================================================

def insert_village_batch(
    cursor,
    village_batch
):

    if not village_batch:

        return 0

    # --------------------------------------------------------
    # Remove duplicate villages inside this batch
    #
    # PostgreSQL error:
    #
    # ON CONFLICT DO UPDATE command cannot affect row
    # a second time
    #
    # happens when the same unique key occurs twice
    # in a single INSERT statement.
    # --------------------------------------------------------

    unique_batch = {}

    for code, name, subdistrict_id in village_batch:

        key = (
            subdistrict_id,
            code
        )

        unique_batch[key] = (
            code,
            name,
            subdistrict_id
        )

    rows = list(
        unique_batch.values()
    )

    # --------------------------------------------------------
    # Batch insert
    # --------------------------------------------------------

    execute_values(
        cursor,
        """
        INSERT INTO villages
            (
                code,
                name,
                sub_district_id
            )
        VALUES %s
        ON CONFLICT (sub_district_id, code)
        DO UPDATE SET
            name = EXCLUDED.name
        """,
        rows,
        page_size=BATCH_SIZE
    )

    return len(rows)


# ============================================================
# IMPORT ONE DATASET
# ============================================================

def import_file(
    connection,
    file_path,
    country_id
):

    df = read_dataset(file_path)

    cursor = connection.cursor()

    # --------------------------------------------------------
    # Caches
    # --------------------------------------------------------

    state_cache = {}

    district_cache = {}

    subdistrict_cache = {}

    # --------------------------------------------------------
    # Village batch
    # --------------------------------------------------------

    village_batch = []

    imported_villages = 0

    skipped_rows = 0

    try:

        # ====================================================
        # PROCESS EVERY ROW
        # ====================================================

        for _, row in df.iterrows():

            # ------------------------------------------------
            # Extract values
            # ------------------------------------------------

            state_code = row["MDDS STC"]

            state_name = row["STATE NAME"]

            district_code = row["MDDS DTC"]

            district_name = row["DISTRICT NAME"]

            subdistrict_code = row["MDDS Sub_DT"]

            subdistrict_name = row[
                "SUB-DISTRICT NAME"
            ]

            village_code = row["MDDS PLCN"]

            village_name = row["Area Name"]

            # ------------------------------------------------
            # Validate state
            # ------------------------------------------------

            if not state_code or not state_name:

                skipped_rows += 1

                continue

            # ------------------------------------------------
            # Validate district
            # ------------------------------------------------

            if not district_code or not district_name:

                skipped_rows += 1

                continue

            # ------------------------------------------------
            # Validate sub-district
            # ------------------------------------------------

            if (
                not subdistrict_code
                or not subdistrict_name
            ):

                skipped_rows += 1

                continue

            # ------------------------------------------------
            # Validate village
            # ------------------------------------------------

            if not village_code or not village_name:

                skipped_rows += 1

                continue

            # ------------------------------------------------
            # STATE
            # ------------------------------------------------

            state_id = get_or_create_state(
                cursor,
                state_cache,
                country_id,
                state_code,
                state_name
            )

            # ------------------------------------------------
            # DISTRICT
            # ------------------------------------------------

            district_id = get_or_create_district(
                cursor,
                district_cache,
                state_id,
                district_code,
                district_name
            )

            # ------------------------------------------------
            # SUB-DISTRICT
            # ------------------------------------------------

            subdistrict_id = get_or_create_subdistrict(
                cursor,
                subdistrict_cache,
                district_id,
                subdistrict_code,
                subdistrict_name
            )

            # ------------------------------------------------
            # Add village
            # ------------------------------------------------

            village_batch.append(
                (
                    village_code,
                    village_name,
                    subdistrict_id
                )
            )

            # ------------------------------------------------
            # Batch insert
            # ------------------------------------------------

            if len(village_batch) >= BATCH_SIZE:

                inserted_count = insert_village_batch(
                    cursor,
                    village_batch
                )

                imported_villages += inserted_count

                connection.commit()

                print(
                    f"  Processed "
                    f"{imported_villages:,} villages..."
                )

                village_batch.clear()

        # ====================================================
        # FINAL BATCH
        # ====================================================

        if village_batch:

            inserted_count = insert_village_batch(
                cursor,
                village_batch
            )

            imported_villages += inserted_count

            connection.commit()

            village_batch.clear()

        # ====================================================
        # FILE SUMMARY
        # ====================================================

        print(
            f"  Imported/processed villages: "
            f"{imported_villages:,}"
        )

        print(
            f"  Skipped rows: "
            f"{skipped_rows:,}"
        )

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()

    return (
        imported_villages,
        skipped_rows
    )


# ============================================================
# DATABASE VERIFICATION
# ============================================================

def verify_database(connection):

    print("\n" + "=" * 60)

    print("DATABASE VERIFICATION")

    print("=" * 60)

    cursor = connection.cursor()

    tables = [
        "countries",
        "states",
        "districts",
        "sub_districts",
        "villages",
    ]

    for table in tables:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        print(
            f"{table:20} : {count:,}"
        )

    # --------------------------------------------------------
    # Orphan checks
    # --------------------------------------------------------

    print("\nHierarchy checks:")

    # States without countries
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM states s
        LEFT JOIN countries c
            ON s.country_id = c.id
        WHERE c.id IS NULL
        """
    )

    orphan_states = cursor.fetchone()[0]

    print(
        f"Orphan states        : {orphan_states:,}"
    )

    # Districts without states
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM districts d
        LEFT JOIN states s
            ON d.state_id = s.id
        WHERE s.id IS NULL
        """
    )

    orphan_districts = cursor.fetchone()[0]

    print(
        f"Orphan districts     : {orphan_districts:,}"
    )

    # Sub-districts without districts
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sub_districts sd
        LEFT JOIN districts d
            ON sd.district_id = d.id
        WHERE d.id IS NULL
        """
    )

    orphan_subdistricts = cursor.fetchone()[0]

    print(
        f"Orphan subdistricts  : {orphan_subdistricts:,}"
    )

    # Villages without sub-districts
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM villages v
        LEFT JOIN sub_districts sd
            ON v.sub_district_id = sd.id
        WHERE sd.id IS NULL
        """
    )

    orphan_villages = cursor.fetchone()[0]

    print(
        f"Orphan villages      : {orphan_villages:,}"
    )

    # --------------------------------------------------------
    # Duplicate checks
    # --------------------------------------------------------

    print("\nDuplicate checks:")

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM (
            SELECT
                sub_district_id,
                code,
                COUNT(*) AS total
            FROM villages
            GROUP BY
                sub_district_id,
                code
            HAVING COUNT(*) > 1
        ) duplicates
        """
    )

    duplicate_villages = cursor.fetchone()[0]

    print(
        f"Duplicate village keys: "
        f"{duplicate_villages:,}"
    )

    cursor.close()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)

    print("MDDS ADDRESS DATA IMPORTER")

    print("=" * 60)

    # ========================================================
    # FIND DATASETS
    # ========================================================

    dataset_files = sorted(
        list(DATA_DIR.glob("*.xls"))
        +
        list(DATA_DIR.glob("*.ods"))
    )

    if not dataset_files:

        print(
            f"ERROR: No .xls or .ods files found "
            f"in {DATA_DIR}"
        )

        sys.exit(1)

    print(
        f"\nDatasets found: "
        f"{len(dataset_files)}"
    )

    for file in dataset_files:

        print(
            f"  - {file.name}"
        )

    connection = None

    try:

        # ====================================================
        # CONNECT
        # ====================================================

        connection = connect_database()

        # ====================================================
        # FIND INDIA
        # ====================================================

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM countries
            WHERE code = 'IN'
            """
        )

        result = cursor.fetchone()

        cursor.close()

        if not result:

            raise RuntimeError(
                "India country record was not found."
            )

        country_id = result[0]

        print(
            f"\nIndia country ID: "
            f"{country_id}"
        )

        # ====================================================
        # IMPORT DATASETS
        # ====================================================

        total_imported = 0

        total_skipped = 0

        for file_number, file_path in enumerate(
            dataset_files,
            start=1
        ):

            print("\n" + "-" * 60)

            print(
                f"[{file_number}/{len(dataset_files)}] "
                f"{file_path.name}"
            )

            print("-" * 60)

            imported, skipped = import_file(
                connection,
                file_path,
                country_id
            )

            total_imported += imported

            total_skipped += skipped

        # ====================================================
        # VERIFY DATABASE
        # ====================================================

        verify_database(connection)

        # ====================================================
        # FINAL SUMMARY
        # ====================================================

        print("\n" + "=" * 60)

        print(
            "IMPORT COMPLETED SUCCESSFULLY"
        )

        print("=" * 60)

        print(
            f"Total imported/processed villages: "
            f"{total_imported:,}"
        )

        print(
            f"Total skipped rows: "
            f"{total_skipped:,}"
        )

    except KeyboardInterrupt:

        print("\n")

        print("=" * 60)

        print(
            "IMPORT INTERRUPTED BY USER"
        )

        print("=" * 60)

        if connection:

            connection.rollback()

        sys.exit(1)

    except Exception as error:

        print("\n")

        print("=" * 60)

        print(
            "IMPORT FAILED"
        )

        print("=" * 60)

        print(error)

        if connection:

            connection.rollback()

        sys.exit(1)

    finally:

        if connection:

            connection.close()

            print(
                "\nDatabase connection closed."
            )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()