import base64
import os
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st
from loguru import logger


def generate_call_graph(
    pyfile: str, format="dot", uses=True, defines=False, grouped=True, colored=True
) -> str:
    with NamedTemporaryFile(mode="w+", encoding="utf8") as f:
        # logger.debug(f"input content: {Path(pyfile).read_text()}")
        logger.debug(f"{f.name=}")
        cmd = ["pyan3", pyfile]
        cmd.append("--uses" if uses else "--no-uses")
        cmd.append("--defines" if defines else "--no-defines")
        if grouped:
            cmd.append("--grouped")
        if colored:
            cmd.append("--colored")
        if format == "dot":
            cmd.append("--dot")
        elif format == "svg":
            cmd.append("--svg")
        elif format == "html":
            cmd.append("--html")
        cmd.append(f">{f.name}")
        logger.debug(f"cmd={' '.join(cmd)}")
        os.system(" ".join(cmd))
        f.seek(0)
        content = f.read()
        # logger.debug(f"{content=}")
        return content
