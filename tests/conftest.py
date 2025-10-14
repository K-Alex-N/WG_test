import random
from collections.abc import Generator

import pytest

from config import (
    COMPONENTS,
    TEMP_DB_NAME,
)
from constants import (
    TEST_RANDOMIZE_ALL_COMPONENTS,
    TEST_RANDOMIZE_ALL_SHIPS,
    TEST_RANDOMIZE_COMPONENT_COMPLETE,
    TEST_RANDOMIZE_SHIP_COMPLETE,
    TEST_RANDOMIZE_TMP_DB_COMPLETED,
    TEST_RANDOMIZE_TMP_DB_START,
)
from db.create_db import create_db
from db.logger import logger
from db.models import ComponentStructure, engine, hull, weapon
from db.seed_db import seed_db
from db.tmp_db import create_tmp_db, drop_tmp_db
from db.utils import get_rand_param_value
from tests.services import ComponentMapper, component_service, ship_service

COMPONENTS_WITH_STRUCTURE = [weapon, hull, engine]


class RandomizeDatabase:
    def __init__(self, db: str):
        self.db = db

    @staticmethod
    def _get_random_component_id(component: str) -> str:
        component_count = ComponentMapper.get_component_count(component)
        return f"{component.capitalize()}-{random.randint(1, component_count)}"

    def _randomize_ship(self, ship_id: str) -> None:
        component = random.choice(COMPONENTS)
        new_component_id = self._get_random_component_id(component)
        ship_service.update_ship_component(
            self.db, ship_id, component, new_component_id
        )
        logger.debug(
            TEST_RANDOMIZE_SHIP_COMPLETE.format(
                ship_id=ship_id, component=component, component_id=new_component_id
            )
        )

    def randomize_ships(self) -> None:
        ships = ship_service.get_all_ships(self.db)
        logger.info(TEST_RANDOMIZE_ALL_SHIPS)

        for ship_id, *_ in ships:
            self._randomize_ship(ship_id)

    def _randomize_component(
        self, component_id: str, comp_structure: ComponentStructure
    ) -> None:
        param_to_change = random.choice(comp_structure.params)
        new_value = get_rand_param_value()

        component_service.update_component_parameter(
            self.db, comp_structure.type, component_id, param_to_change, new_value
        )

        logger.debug(
            TEST_RANDOMIZE_COMPONENT_COMPLETE.format(
                component_id=component_id, param=param_to_change, value=new_value
            )
        )

    def randomize_components(self) -> None:
        for comp_structure in COMPONENTS_WITH_STRUCTURE:
            components = component_service.get_all_components(
                self.db, comp_structure.table_name
            )

            logger.info(
                TEST_RANDOMIZE_ALL_COMPONENTS.format(
                    count=len(components), component_type=comp_structure.type
                )
            )

            for component_id, *_ in components:
                self._randomize_component(component_id, comp_structure)


@pytest.fixture(scope="session", autouse=True)
def db() -> None:
    """Set up main database"""
    create_db()
    seed_db()


@pytest.fixture(scope="session")
def tmp_db() -> Generator:
    """Create temporary db copy"""
    try:
        create_tmp_db()
        yield
    finally:
        drop_tmp_db()


@pytest.fixture(scope="session")
def randomize_tmp_db(tmp_db) -> None:
    logger.info(TEST_RANDOMIZE_TMP_DB_START)

    randomize_db = RandomizeDatabase(TEMP_DB_NAME)
    randomize_db.randomize_ships()
    randomize_db.randomize_components()

    logger.info(TEST_RANDOMIZE_TMP_DB_COMPLETED)
