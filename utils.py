import base64
import os
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st
from loguru import logger


def generate_call_graph(
    pyfile: str,
    format="dot",
    uses=True,
    defines=False,
    grouped=True,
    colored=True,
    rankdir="TB",
) -> str:
    with NamedTemporaryFile(mode="w+", encoding="utf8", delete=False) as f:
        # logger.debug(f"input content: {Path(pyfile).read_text()}")
        logger.debug(f"output file: {f.name}, format: {format}")
        cmd = ["pyan3", pyfile]
        cmd.append("--uses" if uses else "--no-uses")
        cmd.append("--defines" if defines else "--no-defines")
        cmd.extend(["--dot-rankdir", rankdir])
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
        # os.system不能捕获异常
        # os.system(" ".join(cmd))
        sp_result = subprocess.run(
            " ".join(cmd), shell=True, check=False, capture_output=True, text=True
        )
        if sp_result.returncode != 0:
            logger.debug(f"{sp_result.returncode}")
            logger.debug(f"{sp_result.stdout}")
            logger.debug(f"{sp_result.stderr}")
        if sp_result.returncode != 0:
            if "KeyError:" in sp_result.stderr:
                return f"ERROR-Your uploaded file may be incomplete."
        f.seek(0)
        content = f.read()
        # logger.debug(f"{content=}")
        return content
