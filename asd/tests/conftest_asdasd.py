"""Test configuration and fixtures for the WG Test project."""

import random
import sqlite3
from pathlib import Path
from typing import List, Tuple

import pytest

from config import (
    COMPONENTS_LIST,
    ENGINES_COUNT,
    HULLS_COUNT,
    TEMP_DB_NAME,
    WEAPONS_COUNT,
    TEST_SHIP_COUNT,
    DB_NAME
)
from db.conn_db import DatabaseError, get_cursor
from db.create_db import create_db, verify_db_schema
from db.logger import logger
from db.models import ComponentStructure, engine, hull, weapon
from db.seed_db import seed_db
from db.tmp_db import create_tmp_db, drop_tmp_db, temp_db_exists
from db.utils import get_rand_param_value, get_random_component_id

COMPONENTS_WITH_STRUCTURE = [weapon, hull, engine]


@pytest.fixture(scope="session", autouse=True)
def setup_main_database() -> None:
    """Set up the main database for testing."""
    try:
        logger.info("Setting up main database for testing")
        
        # Check if database already exists and has data
        if Path(DB_NAME).exists():
            logger.info("Database already exists, checking if it has data")
            with get_cursor(DB_NAME) as cursor:
                cursor.execute("SELECT COUNT(*) FROM ships")
                ship_count = cursor.fetchone()[0]
                if ship_count > 0:
                    logger.info(f"Database already has {ship_count} ships, skipping seeding")
                    if not verify_db_schema(DB_NAME):
                        raise DatabaseError("Main database schema verification failed")
                    return
        
        # Create and seed database if it doesn't exist or is empty
        create_db(DB_NAME)
        seed_db(DB_NAME)
        
        if not verify_db_schema(DB_NAME):
            raise DatabaseError("Main database schema verification failed")
        
        logger.info("Main database setup completed successfully")
    except Exception as e:
        logger.error(f"Failed to setup main database: {e}")
        raise


def get_max_for_component(component: str) -> int:
    """
    Get the maximum count for a component type.
    
    Args:
        component: Component type name
        
    Returns:
        Maximum count for the component type
        
    Raises:
        ValueError: If component type is unknown
    """
    max_for_component = {
        "weapon": WEAPONS_COUNT,
        "hull": HULLS_COUNT,
        "engine": ENGINES_COUNT,
    }.get(component)

    if not max_for_component:
        raise ValueError(f"Unknown component '{component}'")

    return max_for_component


def get_all_ships(cursor: sqlite3.Cursor) -> List[Tuple]:
    """Get all ships from the database."""
    return cursor.execute("SELECT * FROM ships").fetchall()


def randomize_ship(cursor: sqlite3.Cursor, ship_id: str) -> None:
    """
    Randomize one component of a ship.
    
    Args:
        cursor: Database cursor
        ship_id: ID of the ship to randomize
    """
    component = random.choice(COMPONENTS_LIST)
    max_count = get_max_for_component(component)
    new_component_id = get_random_component_id(component, max_count)
    
    cursor.execute(
        f"UPDATE ships SET {component} = ? WHERE ship = ?",
        (new_component_id, ship_id),
    )
    logger.debug(f"Randomized {component} for ship {ship_id}: {new_component_id}")


def randomize_ships(cursor: sqlite3.Cursor) -> None:
    """
    Randomize all ships in the database.
    
    Args:
        cursor: Database cursor
    """
    ships = get_all_ships(cursor)
    logger.info(f"Randomizing {len(ships)} ships")

    for ship_id, *_ in ships:
        randomize_ship(cursor, ship_id)


def get_all_components(cursor: sqlite3.Cursor, component_db: str) -> List[Tuple]:
    """Get all components from a specific component table."""
    return cursor.execute(f"SELECT * FROM {component_db}").fetchall()


def randomize_component(
    cursor: sqlite3.Cursor, component_id: str, comp_structure: ComponentStructure
) -> None:
    """
    Randomize one parameter of a component.
    
    Args:
        cursor: Database cursor
        component_id: ID of the component to randomize
        comp_structure: Component structure definition
    """
    param_to_change = random.choice(comp_structure.params)
    new_value = get_rand_param_value()

    cursor.execute(
        f"UPDATE {comp_structure.db_name} "
        f"SET {param_to_change} = ? "
        f"WHERE {comp_structure.name} = ? ",
        (new_value, component_id),
    )
    logger.debug(f"Randomized {param_to_change} for {component_id}: {new_value}")


def randomize_components(cursor: sqlite3.Cursor) -> None:
    """
    Randomize all components in the database.
    
    Args:
        cursor: Database cursor
    """
    for comp_structure in COMPONENTS_WITH_STRUCTURE:
        components = get_all_components(cursor, comp_structure.db_name)
        logger.info(f"Randomizing {len(components)} {comp_structure.name} components")

        for component_id, *_ in components:
            randomize_component(cursor, component_id, comp_structure)


@pytest.fixture(scope="session")
def tmp_db():
    """Create and manage temporary database for testing."""
    try:
        logger.info("Creating temporary database for testing")
        create_tmp_db()
        yield
    finally:
        logger.info("Cleaning up temporary database")
        drop_tmp_db()


@pytest.fixture(scope="session", autouse=True)
def randomize_tmp_db(tmp_db):
    """Randomize the temporary database for testing."""
    try:
        logger.info("Randomizing temporary database")
        with get_cursor(TEMP_DB_NAME) as cursor:
            randomize_ships(cursor)
            randomize_components(cursor)
        logger.info("Temporary database randomization completed")
    except Exception as e:
        logger.error(f"Failed to randomize temporary database: {e}")
        raise


@pytest.fixture
def test_ship_ids() -> List[str]:
    """Get list of ship IDs for testing."""
    return [f"Ship-{i}" for i in range(1, TEST_SHIP_COUNT + 1)]


@pytest.fixture
def component_types() -> List[str]:
    """Get list of component types for testing."""
    return COMPONENTS_LIST.copy()
