import sqlite3
import random
import shutil
import os

import pytest

DB_PATH = "spaceship_game.db"
TEMP_DB_PATH = "temp_spaceship_game.db"


def randomize_component(cursor, component_table, component_id_col, component_id, param_choices):
    # Pick one parameter to change
    param_to_change = random.choice(param_choices)
    new_value = random.randint(1, 20)
    cursor.execute(f"""
        UPDATE {component_table}
        SET {param_to_change} = ?
        WHERE {component_id_col} = ?
    """, (new_value, component_id))


@pytest.fixture(scope="session")
def randomized_database():
    # Copy the original database to a temporary one
    if os.path.exists(TEMP_DB_PATH):
        os.remove(TEMP_DB_PATH)
    shutil.copy(DB_PATH, TEMP_DB_PATH)

    conn = sqlite3.connect(TEMP_DB_PATH)
    cursor = conn.cursor()

    # Get all ships
    # cursor.execute("SELECT ship, weapon, hull, engine FROM ships")
    cursor.execute("SELECT * FROM ships") # почему не вот так?
    ships = cursor.fetchall()

    for ship_name, weapon_id, hull_id, engine_id in ships:
        # Randomly choose one component to modify
        component = random.choice(["weapon", "hull", "engine"])

        if component == "weapon":
            randomize_component(
                cursor,
                "weapons",
                "weapon",
                weapon_id,
                ["reload_speed", "rotational_speed", "diameter", "power_volley", "count"]
            )
        elif component == "hull":
            randomize_component(
                cursor,
                "hulls",
                "hull",
                hull_id,
                ["armor", "type", "capacity"]
            )
        elif component == "engine":
            randomize_component(
                cursor,
                "engines",
                "engine",
                engine_id,
                ["power", "type"]
            )

    conn.commit()
    conn.close()

    # в трай-эксепт наверное надо обернуть работу с БД

    yield TEMP_DB_PATH

    if os.path.exists(TEMP_DB_PATH):
        os.remove(TEMP_DB_PATH)
