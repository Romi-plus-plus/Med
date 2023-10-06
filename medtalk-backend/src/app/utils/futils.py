import os
from pathlib import Path
from uuid import uuid1
from fastapi import UploadFile


async def save_file(file: UploadFile) -> str:
    pt = Path("..") / "static" / "images" / f"{uuid1()}{os.path.splitext(file.filename or '')[1]}"
    with open(pt, "wb") as f:
        f.write(await file.read())
    return pt.relative_to("..").as_posix()
