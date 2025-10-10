import shutil
import os

from config import TEMP_DB_NAME, DB_NAME


def copy_db() -> str:
    if os.path.exists(TEMP_DB_NAME):
        os.remove(TEMP_DB_NAME)
    shutil.copy(DB_NAME, TEMP_DB_NAME)
    return TEMP_DB_NAME


