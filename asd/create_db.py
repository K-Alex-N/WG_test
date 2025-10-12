"""Database creation and schema management."""

from typing import List

from config import DB_NAME
from db.conn_db import DatabaseError, get_cursor
from db.logger import logger
from db.tmp_db import drop_db_if_exists


class DatabaseSchema:
    """Database schema definitions and management."""
    
    WEAPONS_TABLE = """
        CREATE TABLE IF NOT EXISTS weapons (
            weapon TEXT PRIMARY KEY,
            reload_speed INTEGER NOT NULL CHECK (reload_speed >= 1 AND reload_speed <= 20),
            rotational_speed INTEGER NOT NULL CHECK (rotational_speed >= 1 AND rotational_speed <= 20),
            diameter INTEGER NOT NULL CHECK (diameter >= 1 AND diameter <= 20),
            power_volley INTEGER NOT NULL CHECK (power_volley >= 1 AND power_volley <= 20),
            count INTEGER NOT NULL CHECK (count >= 1 AND count <= 20)
        );
    """
    
    HULLS_TABLE = """
        CREATE TABLE IF NOT EXISTS hulls (
            hull TEXT PRIMARY KEY,
            armor INTEGER NOT NULL CHECK (armor >= 1 AND armor <= 20),
            type INTEGER NOT NULL CHECK (type >= 1 AND type <= 20),
            capacity INTEGER NOT NULL CHECK (capacity >= 1 AND capacity <= 20)
        );
    """
    
    ENGINES_TABLE = """
        CREATE TABLE IF NOT EXISTS engines (
            engine TEXT PRIMARY KEY,
            power INTEGER NOT NULL CHECK (power >= 1 AND power <= 20),
            type INTEGER NOT NULL CHECK (type >= 1 AND type <= 20)
        );
    """
    
    SHIPS_TABLE = """
        CREATE TABLE IF NOT EXISTS ships (
            ship TEXT PRIMARY KEY,
            weapon TEXT NOT NULL,
            hull TEXT NOT NULL,
            engine TEXT NOT NULL,
            FOREIGN KEY (weapon) REFERENCES weapons(weapon) ON DELETE CASCADE,
            FOREIGN KEY (hull) REFERENCES hulls(hull) ON DELETE CASCADE,
            FOREIGN KEY (engine) REFERENCES engines(engine) ON DELETE CASCADE
        );
    """
    
    # Indexes for better performance
    INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_ships_weapon ON ships(weapon);",
        "CREATE INDEX IF NOT EXISTS idx_ships_hull ON ships(hull);",
        "CREATE INDEX IF NOT EXISTS idx_ships_engine ON ships(engine);",
    ]
    
    @classmethod
    def get_all_tables(cls) -> List[str]:
        """Get all table creation statements."""
        return [
            cls.WEAPONS_TABLE,
            cls.HULLS_TABLE,
            cls.ENGINES_TABLE,
            cls.SHIPS_TABLE,
        ]


def create_db(db_name: str = "WoW.db") -> None:
    """
    Create database with all tables and indexes.
    
    Args:
        db_name: Name of the database to create
        
    Raises:
        DatabaseError: If database creation fails
    """
    try:
        logger.info(f"Creating database: {db_name}")
        drop_db_if_exists(db_name)
        
        with get_cursor(db_name) as cursor:
            # Create tables
            for table_sql in DatabaseSchema.get_all_tables():
                logger.debug(f"Creating table with SQL: {table_sql.strip()}")
                cursor.execute(table_sql)
            
            # Create indexes
            for index_sql in DatabaseSchema.INDEXES:
                logger.debug(f"Creating index with SQL: {index_sql.strip()}")
                cursor.execute(index_sql)
        
        logger.info(f"Database {db_name} created successfully with all tables and indexes")
        
    except Exception as e:
        logger.error(f"Failed to create database {db_name}: {e}")
        raise DatabaseError(f"Database creation failed: {e}") from e


def verify_db_schema(db_name: str = "WoW.db") -> bool:
    """
    Verify that the database schema is correct.
    
    Args:
        db_name: Name of the database to verify
        
    Returns:
        True if schema is correct, False otherwise
    """
    try:
        with get_cursor(db_name) as cursor:
            # Check if all required tables exist
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('weapons', 'hulls', 'engines', 'ships')
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = {'weapons', 'hulls', 'engines', 'ships'}
            if set(tables) != required_tables:
                logger.error(f"Missing tables. Found: {tables}, Required: {required_tables}")
                return False
            
            logger.info(f"Database schema verification successful for {db_name}")
            return True
            
    except Exception as e:
        logger.error(f"Schema verification failed for {db_name}: {e}")
        return False
