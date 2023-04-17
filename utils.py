import base64
import os
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
import streamlit as st

from loguru import logger


def generate_call_graph(pyfile: str, format='dot', **kwargs) -> str:
    with NamedTemporaryFile(mode='w+', encoding='utf8') as f:
        logger.debug(f"input content: {Path(pyfile).read_text()}")
        logger.debug(f"{f.name=}")
        if format == 'dot':
            # cmd = ['pyan3', pyfile, '--uses', '--no-defines', '--colored', '--grouped', '--annotated', '--dot', f'>{f.name}']
            cmd = ['pyan3', pyfile, '--uses', '--no-defines', '--colored', '--grouped', '--dot', f'>{f.name}']
            # subprocess.run(cmd, check=True)
        elif format == 'svg':
            cmd = ['pyan3', pyfile, '--uses', '--no-defines', '--colored', '--grouped', '--svg', f'>{f.name}']
        elif format == 'html':
            cmd = ['pyan3', pyfile, '--uses', '--no-defines', '--colored', '--grouped', '--html', f'>{f.name}']
        logger.debug(f"cmd={' '.join(cmd)}")
        os.system(' '.join(cmd))
        f.seek(0)
        content = f.read()
        logger.debug(f"{content=}")
        return content
