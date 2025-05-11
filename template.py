import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


list_of_files = [
    "core/__init__.py",
    "core/config.py",
    "core/enums.py",
    "db/__init__.py",
    "db/base.py",
    "db/session.py",
    "models/__init__.py",
    "models/video.py",
    "schemas/video.py",
    "api/__init__.py",
    "api/v1/__init__.py",
    "api/v1/endpoints/__init__.py",
    "api/v1/endpoints/video.py",
    ".env",
    "requirements.txt",
    "main.py",
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)


    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")