"""Temporary database management with improved error handling."""

import os
import shutil
from pathlib import Path
from typing import Optional

from config import DB_PATH, TEMP_DB_PATH
# from db.conn_db import DatabaseError
from db.logger import logger


def drop_db_if_exists(db_name: str) -> None:
    """
    Remove database file if it exists.
    
    Args:
        db_name: Name of the database file to remove
    """
    db_path = Path(db_name)
    if db_path.exists():
        try:
            db_path.unlink()
            logger.debug(f"Removed existing database: {db_path}")
        except OSError as e:
            logger.error(f"Failed to remove database {db_path}: {e}")
            raise DatabaseError(f"Failed to remove database: {e}") from e


def create_tmp_db() -> None:
    """
    Create a temporary database by copying the main database.
    
    Raises:
        DatabaseError: If temporary database creation fails
    """
    try:
        if not DB_PATH.exists():
            raise DatabaseError(f"Source database {DB_PATH} does not exist")
        
        # Remove existing temp database if it exists
        drop_db_if_exists(str(TEMP_DB_PATH))
        
        # Copy the main database to create temp database
        shutil.copy2(DB_PATH, TEMP_DB_PATH)
        logger.info(f"Created temporary database: {TEMP_DB_PATH}")
        
    except Exception as e:
        logger.error(f"Failed to create temporary database: {e}")
        raise DatabaseError(f"Temporary database creation failed: {e}") from e


def drop_tmp_db() -> None:
    """
    Remove the temporary database.
    
    Raises:
        DatabaseError: If temporary database removal fails
    """
    try:
        drop_db_if_exists(str(TEMP_DB_PATH))
        logger.info(f"Removed temporary database: {TEMP_DB_PATH}")
    except Exception as e:
        logger.error(f"Failed to remove temporary database: {e}")
        raise DatabaseError(f"Temporary database removal failed: {e}") from e


def temp_db_exists() -> bool:
    """
    Check if temporary database exists.
    
    Returns:
        True if temporary database exists, False otherwise
    """
    return TEMP_DB_PATH.exists()


def get_temp_db_size() -> Optional[int]:
    """
    Get the size of the temporary database file.
    
    Returns:
        Size in bytes if file exists, None otherwise
    """
    if temp_db_exists():
        return TEMP_DB_PATH.stat().st_size
    return None
