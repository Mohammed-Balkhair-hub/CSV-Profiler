from __future__ import annotations
from pathlib import Path
import json


from csv_profiler.profiling import profile_rows
from csv_profiler.io import read_csv_rows


def md_header(title: str, subtitle: str | None = None) -> str:
    text = "# " + title + "\n"
    if subtitle:
        text += subtitle + "\n"
    text += "\n"
    return text


def write_json(report: dict, path: str | Path) -> None:
    with open(path, "w") as f:
        json.dump(report, f, indent=2)




def render_markdown(report: dict, path: str | Path) -> None:
    with open(path, "w") as f:
        # 1- title
        f.write(md_header("CSV Profiling Report"))

        # 2- summary
        summary = report.get("summary", {})
        rows = summary.get("rows", 0)
        cols_count = summary.get("columns", 0)

        f.write("## Summary\n")
        f.write(f"- rows: {rows}\n")
        f.write(f"- columns: {cols_count}\n\n")

        # 3- columns overview table
        f.write("## Columns overview\n")
        f.write("| column | type | missing % | unique |\n")
        f.write("|--------|------|-----------|--------|\n")

        columns = report.get("columns", {})
        for name, data in columns.items():
            col_type = data.get("type", "text")
            stats = data.get("stats", {})
            missing = stats.get("missing", 0)
            unique = stats.get("unique", 0)
            if rows:
                missing_pct = (missing / rows) * 100.0
            else:
                missing_pct = 0.0
            f.write(f"| {name} | {col_type} | {missing_pct:.1f}% | {unique} |\n")

        f.write("\n")

        # 4- per-column details section
        f.write("## Column details\n")
        for name, data in columns.items():
            f.write(f"### {name}\n")
            col_type = data.get("type", "text")
            f.write(f"- type: {col_type}\n")

            stats = data.get("stats", {})
            if col_type == "number":
                f.write(f"- min: {stats.get('min', 0)}\n")
                f.write(f"- max: {stats.get('max', 0)}\n")
                f.write(f"- mean: {stats.get('mean', 0)}\n")
                f.write(f"- median: {stats.get('median', 0)}\n")
            else:
                f.write("- top values:\n")
                for value, cnt in stats.get("top", []):
                    f.write(f"  - {value}: {cnt}\n")

            f.write("\n")
            



if __name__ == "__main__":
    write_json(profile_rows(read_csv_rows("../../data/sample.csv")),"../../outputs/report.json")
    render_markdown(profile_rows(read_csv_rows("../../data/sample.csv")),"../../outputs/report.md")