from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")


def read_dataset(file_path):
    """Read XLS or ODS file as strings."""

    suffix = file_path.suffix.lower()

    if suffix == ".xls":
        return pd.read_excel(
            file_path,
            dtype=str,
            engine="xlrd"
        )

    elif suffix == ".ods":
        return pd.read_excel(
            file_path,
            dtype=str,
            engine="odf"
        )

    else:
        raise ValueError(f"Unsupported file type: {suffix}")


def inspect_file(file_path):
    print("\n" + "=" * 80)
    print(f"FILE: {file_path.name}")
    print("=" * 80)

    try:
        df = read_dataset(file_path)

        print(f"Rows: {len(df):,}")
        print(f"Columns: {len(df.columns)}")

        print("\nColumns:")
        for column in df.columns:
            print(f"  - {column}")

        print("\nMissing values:")
        missing = df.isnull().sum()

        for column, count in missing.items():
            print(f"  {column}: {count:,}")

        print(f"\nDuplicate rows: {df.duplicated().sum():,}")

        print("\nFirst 3 rows:")
        print(df.head(3).to_string(index=False))

    except Exception as error:
        print(f"ERROR: {error}")


def main():
    files = sorted(
        [
            file
            for file in DATA_DIR.iterdir()
            if file.suffix.lower() in [".xls", ".ods", ".xlsx"]
        ]
    )

    print(f"\nFound {len(files)} dataset files.")

    for file_path in files:
        inspect_file(file_path)

    print("\n" + "=" * 80)
    print("INSPECTION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()