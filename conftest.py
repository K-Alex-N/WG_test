import random

import pytest

from config import WEAPONS_COUNT, HULLS_COUNT, ENGINES_COUNT
from db.conn_db import conn_db
from db.copy_db import copy_db
from db.seed_db import seed_db
from db.create_db import create_db


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


def get_random_component(component):
    max_for_component = {
        "weapon": WEAPONS_COUNT,
        "hull": HULLS_COUNT,
        "engine": ENGINES_COUNT
    }.get(component)

    return f"{component}-{random.randint(1, max_for_component)}"


def randomize_ships(cursor):
    ships = cursor.execute("SELECT * FROM ships").fetchall()

    for ship_id, *data in ships:
        component = random.choice(["weapon", "hull", "engine"])

        new_component = get_random_component(component)

        cursor.execute(f"UPDATE ships "
                       f"SET {component} = {new_component} "
                       f"WHERE ship = {ship_id}")

        # component_db = component_to_db[component]
        # cursor.execute(f"UPDATE {component_db} SET {param} = ? WHERE weapon = ?"
        #
        # pass

        # pytest.fail(e) использовать

        # может быть создать ДАТАКЛАССЫ или МОДЕЛЬКИ для каждой БД.
        # ЧТОБЫ потом через точку доставать нужный параметр!!!!
        #
        # можно валидацию через Пайдентик сделать

        # def randomize_components():
        #     # randomize hulls
        #     # randomize hulls
        #     # randomize hulls
        #     pass

        # @ pytest.fixture(scope='session')


@pytest.fixture(scope='session')
def changed_db():
    tmp_db_name = copy_db()
    # conn = conn_db(tmp_db_name)
    with conn_db(tmp_db_name) as conn:
        cursor = conn.cursor()

        randomize_ships(cursor)
        # randomize_components(cursor)
