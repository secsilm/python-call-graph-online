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
clicked = st.button("Generate")
if clicked:
    with NamedTemporaryFile(mode="w+", encoding="utf8") as f:
        logger.debug(f"{code=}")
        f.write(code)
        f.seek(0)
        data = utils.generate_call_graph(f.name, format="svg")
        html = utils.generate_call_graph(f.name, format="html")
    # logger.info(f"{dot=}")
    # st.graphviz_chart(dot)
    st.image(data)
    st.download_button(
        "Download interactive html", html, file_name="python-cg.html", mime="text/html"
    )
