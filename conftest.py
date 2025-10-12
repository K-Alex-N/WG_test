import random
from dataclasses import dataclass

import pytest

from config import (
    COMPONENTS_LIST,
    ENGINES_COUNT,
    HULLS_COUNT,
    TEMP_DB_NAME,
    WEAPONS_COUNT,
)
from db.conn_db import get_cursor
from db.copy_db import create_tmp_db, drop_tmp_db
from db.create_db import create_db
from db.seed_db import seed_db
from db.utils import get_int_from_1_to_20


@pytest.fixture(scope="session", autouse=True)
def db():
    create_db()
    seed_db()


@dataclass
class Component:
    name: str
    params: list[str]
    db_name: str
    max_component_count: int


# fmt: off
weapon = Component(
    "weapon",
    ["reload_speed", "rotational_speed", "diameter", "power_volley", "count"],
    "weapons",
    WEAPONS_COUNT
)

hull = Component(
    "hull",
    ["armor", "type", "capacity"],
    "hulls",
    HULLS_COUNT
)

engine = Component(
    "engine",
    ["power", "type"],
    "engines",
    ENGINES_COUNT
)


def get_random_component(component):
    max_for_component = {
        "Weapon": WEAPONS_COUNT,
        "Hull": HULLS_COUNT,
        "Engine": ENGINES_COUNT
    }.get(component)

    return f"{component}-{random.randint(1, max_for_component)}"

# fmt: on


def get_all_ships(cursor):
    return cursor.execute("SELECT * FROM ships").fetchall()


def randomize_ships(cursor):
    ships = get_all_ships(cursor)

    for ship_id, *_ in ships:
        component = random.choice(COMPONENTS_LIST).capitalize()
        new_component = get_random_component(component)
        cursor.execute(
            f"""
            UPDATE ships 
            SET {component} = ?
            WHERE ship = ? """,
            (new_component, ship_id),
        )


def randomize_components(cursor):
    for component in [weapon, hull, engine]:  # todo
        cursor.execute(f"SELECT * FROM {component.db_name}")
        component_db_data = cursor.fetchall()

        for component_id, *_ in component_db_data:
            param_to_change = random.choice(component.params)
            new_value = get_int_from_1_to_20()

            cursor.execute(
                f"""
                UPDATE {component.db_name}
                SET {param_to_change} = ?
                WHERE {component.name} = ? """,
                (new_value, component_id),
            )


@pytest.fixture(scope="session", autouse=True)
def randomize_tmp_db():
    create_tmp_db()
    with get_cursor(TEMP_DB_NAME) as cursor:
        randomize_ships(cursor)
        randomize_components(cursor)

    yield
    drop_tmp_db()
