import random

import pytest
from db.models import weapon, hull, engine
from config import (
    COMPONENTS_LIST,
    ENGINES_COUNT,
    HULLS_COUNT,
    TEMP_DB_NAME,
    WEAPONS_COUNT,
)
from db.conn_db import get_cursor
from db.tmp_db import create_tmp_db, drop_tmp_db
from db.create_db import create_db
from db.seed_db import seed_db
from db.utils import get_int_from_1_to_20

COMPONENTS_WITH_STRUCTURE = [weapon, hull, engine]


@pytest.fixture(scope="session", autouse=True)
def db():
    create_db()
    seed_db()


def get_max_for_component(component: str) -> int:
    return {
        "weapon": WEAPONS_COUNT,
        "hull": HULLS_COUNT,
        "engine": ENGINES_COUNT,
    }.get(component)


def get_random_component_id(component: str) -> str:
    max_for_component = get_max_for_component(component)
    return f"{component.capitalize()}-{random.randint(1, max_for_component)}"


def get_all_ships(cursor):
    return cursor.execute("SELECT * FROM ships").fetchall()


def randomize_ship(cursor, ship_id: str) -> None:
    component = random.choice(COMPONENTS_LIST)
    new_component_id = get_random_component_id(component)
    cursor.execute(
        f"UPDATE ships SET {component} = ? WHERE ship = ?",
        (new_component_id, ship_id),
    )


def randomize_ships(cursor):
    ships = get_all_ships(cursor)

    for ship_id, *_ in ships:
        randomize_ship(cursor, ship_id)


def get_all_components(cursor, component_db):
    return cursor.execute(f"SELECT * FROM {component_db}").fetchall()


def randomize_component(cursor, component_id, comp_structure):
    param_to_change = random.choice(comp_structure.params)
    new_value = get_int_from_1_to_20()

    cursor.execute(
        f"UPDATE {comp_structure.db_name} "
        f"SET {param_to_change} = ? "
        f"WHERE {comp_structure.name} = ? ",
        (new_value, component_id),
    )


def randomize_components(cursor):
    for comp_structure in COMPONENTS_WITH_STRUCTURE:
        components = get_all_components(cursor, comp_structure.db_name)

        for component_id, *_ in components:
            randomize_component(cursor, component_id, comp_structure)


@pytest.fixture(scope="session", autouse=True)
def randomize_tmp_db():
    create_tmp_db()
    with get_cursor(TEMP_DB_NAME) as cursor:
        randomize_ships(cursor)
        randomize_components(cursor)

    yield
    drop_tmp_db()
