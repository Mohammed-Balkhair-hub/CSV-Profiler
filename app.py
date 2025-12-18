import streamlit as st
import csv 
from io import StringIO
from csv_profiler.profiling  import profile_rows
from csv_profiler.render import render_markdown
import json


st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")
st.caption("Week 01 • Day 04 — Streamlit GUI")



# get the input
st.sidebar.header("Inputs")
source = st.sidebar.selectbox("Data source", ["Upload", "Local path"])
st.write("Selected:", source)
if source =="Upload":
    uploaded = st.sidebar.file_uploader("Upload a CSV", type=["csv"])
else:
    uploaded=None


if uploaded is not None:
    # print some info
    st.write("Filename:", uploaded.name)
    

    #extract data
    raw = uploaded.getvalue()  # bytes
    text = raw.decode("utf-8-sig")
    rows = list(csv.DictReader(StringIO(text)))

    if st.button("Generate report"):
        st.session_state["report"] = profile_rows(rows)
        

report=st.session_state.get("report")
if report is not None:
    show_preview = st.checkbox("Show preview", value=True)
    cols = st.columns(2)
    cols[0].metric("Rows", report["summary"]["rows"])
    cols[1].metric("Columns", report["summary"]["columns"])  

    json_text = json.dumps(report, indent=2, ensure_ascii=False)
    md_text = render_markdown(report)

    l, r = st.columns(2)
    l.download_button("Get JSON", data=json_text, file_name="report.json")
    r.download_button("Get Markdown", data=md_text, file_name="report.md")          
    if show_preview:        
        with st.expander("See explanation"):
            st.subheader("Markdown preview")
            st.markdown(md_text)




