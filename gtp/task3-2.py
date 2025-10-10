import os
import random
import shutil
import sqlite3
from contextlib import closing

import pytest

DB_PATH = "spaceship_game.db"
TEMP_DB_PATH = "temp_spaceship_game.db"


def randomize_component(cursor, table, id_col, component_id, fields):
    """Меняет одно случайное поле в компоненте на случайное значение (1–20)."""
    field = random.choice(fields)
    new_value = random.randint(1, 20)
    cursor.execute(
        f"UPDATE {table} SET {field} = ? WHERE {id_col} = ?",
        (new_value, component_id),
    )


@pytest.fixture(scope="session")
def randomized_database():
    """Создаёт временную копию БД и случайно изменяет по одному параметру у компонентов каждого корабля."""

    # --- Копируем исходную БД ---
    if os.path.exists(TEMP_DB_PATH):
        os.remove(TEMP_DB_PATH)
    shutil.copy(DB_PATH, TEMP_DB_PATH)

    try:
        with closing(sqlite3.connect(TEMP_DB_PATH)) as conn, conn:  # conn.commit() вызовется автоматически
            cursor = conn.cursor()
            cursor.execute("SELECT ship, weapon, hull, engine FROM ships")  # Лучше явно указать поля
            ships = cursor.fetchall()

            for ship_name, weapon_id, hull_id, engine_id in ships:
                component_type = random.choice(["weapon", "hull", "engine"])

                if component_type == "weapon":
                    randomize_component(
                        cursor,
                        "weapons",
                        "weapon",
                        weapon_id,
                        ["reload_speed", "rotational_speed", "diameter", "power_volley", "count"],
                    )
                elif component_type == "hull":
                    randomize_component(
                        cursor,
                        "hulls",
                        "hull",
                        hull_id,
                        ["armor", "type", "capacity"],
                    )
                elif component_type == "engine":
                    randomize_component(
                        cursor,
                        "engines",
                        "engine",
                        engine_id,
                        ["power", "type"],
                    )

    except sqlite3.Error as e:
        pytest.fail(f"Database operation failed: {e}")

    yield TEMP_DB_PATH

    # --- Удаляем временный файл после тестов ---
    if os.path.exists(TEMP_DB_PATH):
        os.remove(TEMP_DB_PATH)
