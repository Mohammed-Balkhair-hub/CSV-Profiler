from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import write_json, render_markdown


def main() -> None:
    rows = read_csv_rows("data/sample.csv")
    report = profile_rows(rows)
    write_json(report, "outputs/report.json")
    render_markdown(report, "outputs/report.md")
    print("Wrote outputs/report.json and outputs/report.md")


if __name__ == "__main__":
    main()