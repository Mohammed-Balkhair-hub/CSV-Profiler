import json
import time
import typer
from pathlib import Path

from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import write_json,create_markdown


app=typer.Typer()

@app.command(help="Profile a CSV file and write JSON + Markdown")
def profile(
    input_path:Path=typer.Argument(..., help="Path to the input CSV file"),
    output_path:Path=typer.Option(Path("outputs"),"--output-path", help="Path to the output directory"),
    report_name:str=typer.Option("report", "--report-name", help="Name of the report file"),
    preview:bool=typer.Option(False, "--preview", help="Preview the report"),):
    try:
        start_time=time.time()

        rows=read_csv_rows(input_path)
        report=profile_rows(rows)
        write_json(report, output_path / f"{report_name}.json")
        create_markdown(report, output_path / f"{report_name}.md")

        end_time=time.time()
        duration=end_time-start_time
        if preview:
            typer.echo(f"rows: {report['summary']['rows']} | columns: {report['summary']['columns']} | duration: {duration:.2f} seconds")
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
