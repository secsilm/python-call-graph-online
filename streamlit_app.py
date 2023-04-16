from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st
from loguru import logger

import utils

st.title('Generate Python Call Graph Online')

st.write('Input your python file content, click Generate and wait a minute, you will see the call graph.')
code = st.text_area(label='Code', placeholder='Please input your Python code here')
clicked = st.button("Generate")
if clicked:
    with NamedTemporaryFile(mode='w+', encoding='utf8') as f:
        logger.debug(f"{code=}")
        f.write(code)
        f.seek(0)
        dot = utils.generate_call_graph(f.name)
    logger.info(f"{dot=}")
    st.graphviz_chart(dot)
