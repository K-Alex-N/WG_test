from dataclasses import dataclass
import random

import pytest

from config import WEAPONS_COUNT, HULLS_COUNT, ENGINES_COUNT, TEMP_DB_NAME, COMPONENTS_LIST
from db.conn_db import conn_db
from db.copy_db import create_tmp_db_copy, drop_tmp_db
from db.seed_db import seed_db
from db.create_db import create_db
from db.utils import get_random_integer


@pytest.fixture(scope='session', autouse=True)
def db():
    create_db()
    seed_db()


@dataclass
class Component:
    name: str
    params: list[str]
    db_name: str
    max_component_count: int


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


def randomize_ships(cursor, conn):
    ships = cursor.execute("SELECT * FROM ships").fetchall()

    for ship_id, *_ in ships:
        component = random.choice(COMPONENTS_LIST).capitalize()

        new_component = get_random_component(component)
        cursor.execute(
            f"UPDATE ships "
            f"SET {component} = ?"
            f"WHERE ship = ?",
            (new_component, ship_id))
        conn.commit()


def randomize_components(cursor, conn):
    # for component in [weapon, "hull", "engine"]:
    for component in [weapon, hull, engine]:  # выбрать первый компонент
        cursor.execute(f"SELECT * FROM {component.db_name}")
        component_db_data = cursor.fetchall()

        for component_id, *_ in component_db_data:
            param_to_change = random.choice(component.params)
            new_value = get_random_integer()

            cursor.execute(f"""
                UPDATE {component.db_name}
                SET {param_to_change} = ?
                WHERE {component.name} = ?
            """, (new_value, component_id))
            conn.commit()


@pytest.fixture(scope='session', autouse=True)
def tmp_changed_db():
    create_tmp_db_copy()
    with conn_db(TEMP_DB_NAME) as conn:
        cursor = conn.cursor()

        randomize_ships(cursor, conn)
        randomize_components(cursor, conn)

    yield
    # drop_tmp_db()
