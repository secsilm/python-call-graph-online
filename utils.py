import subprocess
from tempfile import NamedTemporaryFile
from loguru import logger
from pathlib import Path
import os


def generate_call_graph(pyfile: str, **kwargs) -> str:
    with NamedTemporaryFile(mode='w+', encoding='utf8') as f:
        logger.debug(f"input content: {Path(pyfile).read_text()}")
        logger.debug(f"{f.name=}")
        # cmd = ['pyan3', pyfile, '--uses', '--no-defines', '--colored', '--grouped', '--annotated', '--dot', f'>{f.name}']
        cmd = ['pyan3', pyfile, '--uses', '--no-defines', '--colored', '--grouped', '--dot', f'>{f.name}']
        logger.debug(f"cmd={' '.join(cmd)}")
        # subprocess.run(cmd, check=True)
        os.system(' '.join(cmd))
        f.seek(0)
        content = f.read()
        logger.debug(f"{content=}")
        return content
