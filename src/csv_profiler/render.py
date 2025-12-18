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




def render_markdown(report: dict) -> str:
    lines=[]
    # 1- title
    lines.append(md_header("CSV Profiling Report"))

    # 2- summary
    summary = report.get("summary", {})
    rows = summary.get("rows", 0)
    cols_count = summary.get("columns", 0)

    lines.append("## Summary\n")
    lines.append(f"- rows: {rows}\n")
    lines.append(f"- columns: {cols_count}\n\n")

    # 3- columns overview table
    lines.append("## Columns overview\n")
    lines.append("| column | type | missing % | unique |\n")
    lines.append("|--------|------|-----------|--------|\n")

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
        lines.append(f"| {name} | {col_type} | {missing_pct:.1f}% | {unique} |\n")

    lines.append("\n")

    # 4- per-column details section
    lines.append("## Column details\n")
    for name, data in columns.items():
        lines.append(f"### {name}\n")
        col_type = data.get("type", "text")
        lines.append(f"- type: {col_type}\n")

        stats = data.get("stats", {})
        if col_type == "number":
            lines.append(f"- min: {stats.get('min', 0)}\n")
            lines.append(f"- max: {stats.get('max', 0)}\n")
            lines.append(f"- mean: {stats.get('mean', 0)}\n")
            lines.append(f"- median: {stats.get('median', 0)}\n")
        else:
            lines.append("- top values:\n")
            for value, cnt in stats.get("top", []):
                lines.append(f"  - {value}: {cnt}\n")

        lines.append("\n")

    return "".join(lines)
            
def create_markdown(report:dict,path)-> None:
    text=render_markdown(report)
    with open(path, mode='w') as f:
        f.write(text)



if __name__ == "__main__":
    write_json(profile_rows(read_csv_rows("../../data/sample.csv")),"../../outputs/report.json")
    render_markdown(profile_rows(read_csv_rows("../../data/sample.csv")),"../../outputs/report.md")