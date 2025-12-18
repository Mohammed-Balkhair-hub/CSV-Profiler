from csv_profiler.io import read_csv_rows
from math import ceil


MISSING = {"","na","n/a","null","none","nan",}

def is_missing(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().casefold() in MISSING # casefold like lower() but case sensitive for comparison


def try_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def infer_type(values: list[str]) -> str:
    numbers = 0
    for v in values:
        if is_missing(v):
            continue
        elif try_float(v) is not None:
            numbers += 1
        else:
            return "string"
    return "number"


def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
    return [row.get(col, "") for row in rows]


def numeric_stats(values: list[str]) -> dict:
    """Compute stats for numeric column values (strings)."""

    usable = []
    for v in values:
        if not is_missing(v):
            usable.append(v)

    nums = []
    for v in usable:
        n = try_float(v)
        if n is None:
            # then maybe it is a string coulmn!
            return {}
        nums.append(n)

    if len(nums) == 0:
        return {}
    
    median=sorted(nums)[ceil(len(nums)/2)]
    count = len(nums)
    unique = len(set(nums))
    minimum = min(nums)
    maximum = max(nums)
    mean = sum(nums) / count

    return {
        "count": count,
        "missing": len(values) - count,
        "unique": unique,
        "min": minimum,
        "max": maximum,
        "mean": mean,
        "median":median,
    }


def text_stats(values: list[str], top_k: int = 5) -> dict:
    usable = []
    for v in values:
        if not is_missing(v):
            usable.append(v)

    counts = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1

    top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_k]

    return {
        "count": len(usable),
        "missing": len(values) - len(usable),
        "unique": len(counts),
        "top": top,
    }


def profile_rows(rows: list[dict[str, str]]) -> dict:
    """Compute high level profile for the CSV rows."""

    report = {}

    summary = {}
    summary["rows"] = len(rows)
    if len(rows) > 0:
        summary["columns"] = len(rows[0])
    else:
        summary["columns"] = 0
    report["summary"] = summary

    columns = {}
    if len(rows) > 0:
        for col in rows[0].keys():
            values = column_values(rows, col)
            col_type = infer_type(values)

            col_info = {}
            col_info["type"] = col_type

            if col_type == "number":
                col_info["stats"] = numeric_stats(values)
            else:
                col_info["stats"] = text_stats(values)

            columns[col] = col_info

    report["columns"] = columns

    return report


if __name__ == "__main__":
    profile_rows(read_csv_rows("../../data/sample.csv"))