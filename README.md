## Welcome to CSV-profiler  Tutorial

!["here the image of the streamlit GUI should appear"](Assets/csv-profiler-img-3.jpg)
## Setup
```markdown
uv sync
```
## Run CLI

## If you have a src/ folder:
*Mac/Linux:*
```
 export PYTHONPATH=src
```
*Windows:*
```
$env:PYTHONPATH="src"
```
### then:
```
uv run python -m csv_profiler.cli  data/sample.csv --output-dir outputs
```

## Run GUI
*Mac/Linux:*
```
 export PYTHONPATH=src
```
*Windows:*
```
$env:PYTHONPATH="src"
```

### then:
```
uv run streamlit run app.py
```