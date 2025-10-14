import random

import pytest

from config import (
    COMPONENTS_LIST,
    TEMP_DB_NAME,
)
from constants import TEST_RANDOMIZE_SHIP_START, TEST_RANDOMIZE_SHIP_COMPLETE, \
    TEST_RANDOMIZE_ALL_SHIPS, TEST_RANDOMIZE_COMPONENT_START, \
    TEST_RANDOMIZE_COMPONENT_COMPLETE, TEST_RANDOMIZE_ALL_COMPONENTS
from db.create_db import create_db
from db.logger import logger
from db.models import ComponentStructure, engine, hull, weapon
from db.seed_db import seed_db
from db.tmp_db import create_tmp_db, drop_tmp_db
from db.utils import get_rand_param_value
from tests.services import ShipService, ComponentService, ComponentMapper

COMPONENTS_WITH_STRUCTURE = [weapon, hull, engine]

ship_service = ShipService()
component_service = ComponentService()


@pytest.fixture(scope="session", autouse=True)
def db() -> None:
    """Set up the main database for testing."""
    create_db()
    seed_db()


def get_random_component_id(component: str) -> str:
    component_count = ComponentMapper.get_component_count(component)
    return f"{component.capitalize()}-{random.randint(1, component_count)}"


def randomize_ship(ship_id: str) -> None:
    logger.debug(TEST_RANDOMIZE_SHIP_START.format(ship_id=ship_id))
    component = random.choice(COMPONENTS_LIST)
    new_component_id = get_random_component_id(component)
    ship_service.update_ship_component(TEMP_DB_NAME, ship_id, component,
                                       new_component_id)
    logger.debug(TEST_RANDOMIZE_SHIP_COMPLETE.format(
        ship_id=ship_id,
        component=component,
        component_id=new_component_id
    ))


def randomize_ships() -> None:
    ships = ship_service.get_all_ships(TEMP_DB_NAME)
    logger.info(TEST_RANDOMIZE_ALL_SHIPS.format(count=len(ships)))

    for ship_id, *_ in ships:
        randomize_ship(ship_id)


def randomize_component(component_id: str, comp_structure: ComponentStructure) -> None:
    """
    Randomize one parameter of a component.

    Uses service layer to update component data.

    Args:
        component_id: Component identifier
        comp_structure: Component structure metadata
    """
    logger.debug(TEST_RANDOMIZE_COMPONENT_START.format(component_id=component_id))
    param_to_change = random.choice(comp_structure.params)
    new_value = get_rand_param_value()

    component_service.update_component_parameter(
        TEMP_DB_NAME,
        comp_structure.type,
        component_id,
        param_to_change,
        new_value
    )

    logger.debug(TEST_RANDOMIZE_COMPONENT_COMPLETE.format(
        component_id=component_id,
        param=param_to_change,
        value=new_value
    ))


def randomize_components() -> None:
    """
    Randomize all components in the temporary database.

    Uses service layer to retrieve and update component data.
    """
    for comp_structure in COMPONENTS_WITH_STRUCTURE:
        components = component_service.get_all_components(
            TEMP_DB_NAME,
            comp_structure.table_name
        )

        logger.info(TEST_RANDOMIZE_ALL_COMPONENTS.format(
            count=len(components),
            component_type=comp_structure.type
        ))

        for component_id, *_ in components:
            randomize_component(component_id, comp_structure)


@pytest.fixture(scope="session")
def tmp_db():
    try:
        # logger.info("Creating temporary database for testing")
        create_tmp_db()
        yield
    finally:
        # logger.info("Cleaning up temporary database")
        drop_tmp_db()


@pytest.fixture(scope="session", autouse=True)
def randomize_tmp_db(tmp_db):
    # logger.info("Randomizing temporary database")
    randomize_ships()
    randomize_components()
    # logger.info("Temporary database randomization completed")


# @pytest.fixture
# def component_types() -> List[str]:
#     """Get list of component types for testing."""
#     return COMPONENTS_LIST.copy()
