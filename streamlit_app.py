from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st
from loguru import logger

import utils

st.title("Generate Python Call Graph Online")
st.write(
    "Input your python file content, click Generate and wait a minute, you will see the call graph. You can also download it as an interactive html."
)

code = st.text_area(label="Code", placeholder="Please input your Python code here")
with st.sidebar:
    uses = st.checkbox("Add edges for 'uses' relationships", value=True)
    defines = st.checkbox("Add edges for 'defines' relationships", value=False)
    grouped = st.checkbox(
        "Group nodes (create subgraphs) according to namespace", value=True
    )
    colored = st.checkbox("Color nodes according to namespace", value=True)
clicked = st.button("Generate")
if clicked:
    with NamedTemporaryFile(mode="w+", encoding="utf8") as f:
        logger.debug(f"{code=}")
        f.write(code)
        f.seek(0)
        data = utils.generate_call_graph(
            f.name, format="svg", defines=defines, grouped=grouped, colored=colored
        )
        html = utils.generate_call_graph(
            f.name, format="html", defines=defines, grouped=grouped, colored=colored
        )
    # logger.info(f"{dot=}")
    # st.graphviz_chart(dot)
    st.image(data)
    st.download_button(
        "Download interactive html", html, file_name="python-cg.html", mime="text/html"
    )
