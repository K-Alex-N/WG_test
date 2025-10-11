import os
import shutil

from config import DB_NAME, TEMP_DB_NAME


def drop_db_if_exists(db_name: str = DB_NAME) -> None:
    if os.path.exists(db_name):
        os.remove(db_name)


def create_tmp_db_copy() -> None:
    drop_db_if_exists(TEMP_DB_NAME)
    shutil.copy(DB_NAME, TEMP_DB_NAME)


def drop_tmp_db() -> None:
    drop_db_if_exists(TEMP_DB_NAME)
