"""Database connection management with improved error handling."""

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from config import DB_PATH, TEMP_DB_PATH
from db.logger import logger


class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass


def get_db_path(db_name: str) -> Path:
    """Get the full path for a database file."""
    if db_name == "WoW.db":
        return DB_PATH
    elif db_name == "temp_WoW.db":
        return TEMP_DB_PATH
    else:
        # If it's a relative path, make it relative to the project root
        if not Path(db_name).is_absolute():
            return Path(db_name)
        return Path(db_name)


@contextmanager
def conn_db(db_name: str = "WoW.db") -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager for database connections with improved error handling.
    
    Args:
        db_name: Name of the database file
        
    Yields:
        SQLite connection object
        
    Raises:
        DatabaseError: If database connection or operation fails
    """
    db_path = get_db_path(db_name)
    
    # Ensure parent directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = None
    try:
        logger.debug(f"Connecting to database: {db_path}")
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row  # Enable column access by name
        yield conn
        conn.commit()
        logger.debug(f"Successfully committed transaction to {db_path}")
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
            logger.error(f"Database error in {db_path}, transaction rolled back: {e}")
        raise DatabaseError(f"Database operation failed: {e}") from e
    except Exception as e:
        if conn:
            conn.rollback()
            logger.error(f"Unexpected error in {db_path}: {e}")
        raise DatabaseError(f"Unexpected database error: {e}") from e
    finally:
        if conn:
            conn.close()
            logger.debug(f"Closed connection to {db_path}")


@contextmanager
def get_cursor(db_name: str = "WoW.db") -> Generator[sqlite3.Cursor, None, None]:
    """
    Context manager for database cursors with improved error handling.
    
    Args:
        db_name: Name of the database file
        
    Yields:
        SQLite cursor object
    """
    with conn_db(db_name) as conn:
        cursor = conn.cursor()
        try:
            yield cursor
        except sqlite3.Error as e:
            logger.error(f"Cursor error in {db_name}: {e}")
            raise DatabaseError(f"Cursor operation failed: {e}") from e
        finally:
            cursor.close()
