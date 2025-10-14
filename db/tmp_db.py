import os
import shutil

from config import DB_NAME, TEMP_DB_NAME
from constants import TMP_DB_CREATED, TMP_DB_REMOVED
from db.logger import logger


def drop_db_if_exists(db_name: str = DB_NAME) -> None:
    if os.path.exists(db_name):
        os.remove(db_name)


def create_tmp_db() -> None:
    drop_db_if_exists(TEMP_DB_NAME)
    shutil.copy(DB_NAME, TEMP_DB_NAME)
    logger.info(TMP_DB_CREATED.format(db_name=TEMP_DB_NAME))


def drop_tmp_db() -> None:
    drop_db_if_exists(TEMP_DB_NAME)
    logger.info(TMP_DB_REMOVED.format(db_name=TEMP_DB_NAME))
