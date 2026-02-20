# nodes/extraction/utils/file_utils.py

import os

def is_pdf(file_path: str) -> bool:
    return file_path.lower().endswith(".pdf")


def validate_file_exists(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")