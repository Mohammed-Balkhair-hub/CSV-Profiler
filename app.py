import streamlit as st
import csv 
from io import StringIO
from csv_profiler.profiling  import profile_rows
from csv_profiler.render import render_markdown
import json


def gradient_header(text, color1, color2, font_size=30, text_color='#FFFFFF'):
    """
    Creates a header with a gradient background using custom CSS.

    Args:
        text (str): The text to display in the header.
        color1 (str): The starting color of the gradient (e.g., '#FF4B4B').
        color2 (str): The ending color of the gradient (e.g., '#26B99A').
        font_size (int): The font size in pixels.
        text_color (str): The color of the header text (e.g., '#FFFFFF').
    """
    st.markdown(f"""
    <p style="
        background-image: linear-gradient(to right, {color1}, {color2});
        color: {text_color};
        font-size: {font_size}px;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    ">{text}</p>
    """, unsafe_allow_html=True)






# Another example with different colors
gradient_header(
    text="CSV Profiler",
    color1="#534F91", #
    color2="#49A4A1", # 
    font_size=50,
    text_color='#ffffff'
)

st.set_page_config(page_title="CSV Profiler", layout="wide")
#st.title("CSV Profiler")
st.caption("Week 01 • SDAIA AI Proffesionals camp")



#SIDEBAR
st.sidebar.write("")
st.sidebar.write("")

# The URL of the image you want to display
image_url = "https://salogos.org/wp-content/uploads/2025/05/0191-1568x545.png"

# Display the image using st.image()
st.sidebar.image(image_url, width=250)

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

    if st.button("Generate Report",type="primary"):
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
    l.download_button("Get JSON", data=json_text, file_name="report.json",type="primary")
    r.download_button("Get Markdown", data=md_text, file_name="report.md",type="primary")          
    if show_preview:        
        with st.expander("See explanation"):
            st.subheader("Markdown preview")
            st.markdown(md_text)

















