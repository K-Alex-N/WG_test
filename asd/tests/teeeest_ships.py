"""Test suite for database comparison and validation."""

from dataclasses import asdict
from typing import List

import pytest

from config import COMPONENTS_LIST, DB_NAME, TEMP_DB_NAME, TEST_SHIP_COUNT
from db.conn_db import DatabaseError, get_cursor
from db.logger import logger
from db.models import Component, Engine, Hull, Ship, Weapon


def get_component_object(comp: str, db_row: tuple) -> Component:
    """
    Create a component object from database row.
    
    Args:
        comp: Component type name
        db_row: Database row tuple
        
    Returns:
        Component object
        
    Raises:
        ValueError: If component type is unknown
    """
    comp_class = {"weapon": Weapon, "hull": Hull, "engine": Engine}.get(comp)
    if comp_class is None:
        raise ValueError(f"Unknown component: '{comp}'")
    return comp_class(*db_row)


def get_ship(db: str, ship_id: str) -> Ship:
    """
    Get a ship from the specified database.
    
    Args:
        db: Database name
        ship_id: Ship ID
        
    Returns:
        Ship object
        
    Raises:
        ValueError: If ship not found
        DatabaseError: If database operation fails
    """
    try:
        with get_cursor(db) as cursor:
            cursor.execute("SELECT * FROM ships WHERE ship=?", (ship_id,))
            row = cursor.fetchone()

        if not row:
            raise ValueError(f"Ship not found: {ship_id}")
        return Ship(*row)
    except Exception as e:
        logger.error(f"Failed to get ship {ship_id} from {db}: {e}")
        raise DatabaseError(f"Failed to get ship: {e}") from e


def get_original_ship(ship_id: str) -> Ship:
    """Get ship from original database."""
    return get_ship(DB_NAME, ship_id)


def get_changed_ship(ship_id: str) -> Ship:
    """Get ship from changed database."""
    return get_ship(TEMP_DB_NAME, ship_id)


def compare_components_in_ship(comp: str, orig_ship: Ship, changed_ship: Ship) -> None:
    """
    Compare components between original and changed ships.
    
    Args:
        comp: Component type to compare
        orig_ship: Original ship
        changed_ship: Changed ship
        
    Raises:
        pytest.fail: If components don't match
    """
    if orig_ship[comp] != changed_ship[comp]:
        logger.debug(f"Component mismatch for {orig_ship.ship_id}, {comp}: "
                    f"expected {orig_ship[comp]}, was {changed_ship[comp]}")
        pytest.fail(
            f"{orig_ship.ship_id}, {comp}\n"
            f"\tExpected {orig_ship[comp]}, was {changed_ship[comp]}"
        )


def compare_params_in_component(orig_comp: Component, changed_comp: Component, ship_id: str) -> None:
    """
    Compare parameters between original and changed components.
    
    Args:
        orig_comp: Original component
        changed_comp: Changed component
        ship_id: Ship ID for error reporting
        
    Raises:
        pytest.fail: If parameters don't match
    """
    orig_comp_dict = asdict(orig_comp)
    changed_comp_dict = asdict(changed_comp)

    for param, value in orig_comp_dict.items():
        if value != changed_comp_dict[param]:
            logger.debug(f"Parameter mismatch for {ship_id}, {changed_comp_dict['comp_id']}, "
                        f"{param}: expected {value}, was {changed_comp_dict[param]}")
            pytest.fail(
                f"{ship_id}, {changed_comp_dict['comp_id']}\n"
                f"\t{param}: expected {value}, was {changed_comp_dict[param]}"
            )


def get_comp(db: str, comp: str, comp_id: str) -> Component:
    """
    Get a component from the specified database.
    
    Args:
        db: Database name
        comp: Component type
        comp_id: Component ID
        
    Returns:
        Component object
        
    Raises:
        ValueError: If component not found
        DatabaseError: If database operation fails
    """
    try:
        comp_db = f"{comp}s"
        with get_cursor(db) as cursor:
            cursor.execute(f"SELECT * FROM {comp_db} WHERE {comp}=?", (comp_id,))
            row = cursor.fetchone()

        if not row:
            raise ValueError(f"Component not found: {comp_id}")
        return get_component_object(comp, row)
    except Exception as e:
        logger.error(f"Failed to get component {comp_id} from {db}: {e}")
        raise DatabaseError(f"Failed to get component: {e}") from e


def get_orig_comp(comp: str, comp_id: str) -> Component:
    """Get component from original database."""
    return get_comp(DB_NAME, comp, comp_id)


def get_changed_comp(comp: str, comp_id: str) -> Component:
    """Get component from changed database."""
    return get_comp(TEMP_DB_NAME, comp, comp_id)


@pytest.mark.parametrize("comp", COMPONENTS_LIST)
@pytest.mark.parametrize("i", range(1, TEST_SHIP_COUNT + 1))
def test_differences_in_databases(comp: str, i: int) -> None:
    """
    Test database differences for ships and components.
    
    This test verifies that:
    1. Ship components (weapon, hull, engine) have been changed
    2. Component parameters have been modified
    
    Args:
        comp: Component type to test
        i: Ship number to test
    """
    ship_id = f"Ship-{i}"
    logger.debug(f"Testing differences for {ship_id}, component: {comp}")

    try:
        # Compare components in ship
        orig_ship = get_original_ship(ship_id)
        changed_ship = get_changed_ship(ship_id)

        compare_components_in_ship(comp, orig_ship, changed_ship)

        # Compare parameters in component
        comp_id = orig_ship[comp]
        orig_comp = get_orig_comp(comp, comp_id)
        changed_comp = get_changed_comp(comp, comp_id)

        compare_params_in_component(orig_comp, changed_comp, ship_id)
        
        logger.debug(f"Test passed for {ship_id}, component: {comp}")
        
    except Exception as e:
        logger.error(f"Test failed for {ship_id}, component: {comp} - {e}")
        raise


def test_database_schema_integrity() -> None:
    """Test that both databases have correct schema."""
    from db.create_db import verify_db_schema
    
    assert verify_db_schema(DB_NAME), "Original database schema is invalid"
    assert verify_db_schema(TEMP_DB_NAME), "Temporary database schema is invalid"


def test_database_has_data() -> None:
    """Test that both databases contain data."""
    with get_cursor(DB_NAME) as cursor:
        cursor.execute("SELECT COUNT(*) FROM ships")
        orig_count = cursor.fetchone()[0]
        
    with get_cursor(TEMP_DB_NAME) as cursor:
        cursor.execute("SELECT COUNT(*) FROM ships")
        temp_count = cursor.fetchone()[0]
    
    assert orig_count > 0, "Original database has no ships"
    assert temp_count > 0, "Temporary database has no ships"
    assert orig_count == temp_count, "Ship counts don't match between databases"
