from __future__  import annotations

from csv import DictReader
from pathlib import Path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read a CSV as a list of rows (each row is a dict of strings)."""
    with open(path, mode='r', newline="") as f:
        reader = DictReader(f)
        rows = []
        for row in reader:
            rows.append(row)
        
        if len(rows) == 0:
            raise ValueError(f"CSV file has no rows")
        
        return rows

if __name__ == "__main__":
    dictionary=read_csv_rows("../../data/sample.csv")
    print(dictionary[0])
        