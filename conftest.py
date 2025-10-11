from dataclasses import dataclass
import random

import pytest

from config import WEAPONS_COUNT, HULLS_COUNT, ENGINES_COUNT
from db.conn_db import conn_db
from db.copy_db import copy_db
from db.seed_db import seed_db
from db.create_db import create_db
from db.utils import get_random_integer


@pytest.fixture(scope='session', autouse=True)
def db():
    create_db()
    seed_db()
    yield
    # drop_db


# component_to_db = {
#     "weapon": "weapons",
#     "hull": "hulls",
#     "engine": "engines",
# }

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

    for ship_id, *data in ships:
        component = random.choice(["Weapon", "Hull", "Engine"])

        new_component = get_random_component(component)
        sql = f"""
            UPDATE ships 
            SET {component} = "{new_component}"
            WHERE ship = "{ship_id}";
        """
        cursor.execute(sql)
        conn.commit()

    # component_db = component_to_db[component]
    # cursor.execute(f"UPDATE {component_db} SET {param} = ? WHERE weapon = ?"
    #
    # pass

    # pytest.fail(e) использовать

    # может быть создать ДАТАКЛАССЫ или МОДЕЛЬКИ для каждой БД.
    # ЧТОБЫ потом через точку доставать нужный параметр!!!!
    #
    # можно валидацию через Пайдентик сделать


# def get_component_table(component) -> str:
#     return component + "s"


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
def changed_db():
    tmp_db_name = copy_db()
    # conn = conn_db(tmp_db_name)
    with conn_db(tmp_db_name) as conn:
        cursor = conn.cursor()

        randomize_ships(cursor, conn)
        randomize_components(cursor, conn)
