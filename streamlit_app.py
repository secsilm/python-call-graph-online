import re
from pathlib import Path
import subprocess
from tempfile import NamedTemporaryFile, TemporaryDirectory

import streamlit as st
from loguru import logger

import utils

st.title("Generate Python Call Graph Online")
st.write(
    """
Usage:

1. Input your python file content (or github link) or upload your python files. If it's a github link, it must start with `https://github.com/`.
2. click `Generate` and wait seconds.
3. You will see the call graph. You can also download it as an interactive html.

⚠️ The file name starting with a number will have an underscore added at the beginning because Graphviz does not support node names starting with a number. See [here](https://graphviz.org/doc/info/lang.html#:~:text=not%20beginning%20with%20a%20digit) and [here](https://patchwork.ozlabs.org/project/buildroot/patch/20181124093452.12350-1-yann.morin.1998@free.fr/) for reference.
"""
)

code = st.text_area(label="Code", placeholder="Please input your Python code here")
uploaded_files = st.file_uploader("Choose python files", accept_multiple_files=True)
with st.sidebar:
    uses = st.checkbox("Add edges for 'uses' relationships", value=True)
    defines = st.checkbox("Add edges for 'defines' relationships", value=False)
    grouped = st.checkbox(
        "Group nodes (create subgraphs) according to namespace", value=True
    )
    colored = st.checkbox("Color nodes according to namespace", value=True)
clicked = st.button("Generate")
if clicked:
    if code:
        if code.startswith('https://github.com/'):
            with TemporaryDirectory() as tmpdir:
                cmd = ['git', 'clone', code, tmpdir]
                logger.info(f"Cloning {code} to {tmpdir}")
                subprocess.run(
                    " ".join(cmd), shell=True, check=False, capture_output=True, text=True
                )
                svg = utils.generate_call_graph(
                    f"{tmpdir}/**/*.py",
                    format="svg",
                    defines=defines,
                    grouped=grouped,
                    colored=colored,
                )
                html = utils.generate_call_graph(
                    f"{tmpdir}/**/*.py",
                    format="html",
                    defines=defines,
                    grouped=grouped,
                    colored=colored,
                )
        else:
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
    else:
        with TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            for uploaded_file in uploaded_files:
                filename = (
                    f"_{uploaded_file.name}"
                    if re.match(r"\d", uploaded_file.name)
                    else uploaded_file.name
                )
                tmpdir.joinpath(filename).write_bytes(uploaded_file.read())
            logger.debug(f"{list(tmpdir.glob('*'))}")
            svg = utils.generate_call_graph(
                f"{tmpdir}/**/*.py",
                format="svg",
                defines=defines,
                grouped=grouped,
                colored=colored,
            )
            html = utils.generate_call_graph(
                f"{tmpdir}/**/*.py",
                format="html",
                defines=defines,
                grouped=grouped,
                colored=colored,
            )
    # logger.info(f"{dot=}")
    # st.graphviz_chart(dot)
    if svg.startswith("ERROR-"):
        st.error(svg.split("-", maxsplit=1)[1])
    else:
        st.image(svg)
        st.download_button(
            "Download interactive html",
            html,
            file_name="python-cg.html",
            mime="text/html",
        )
