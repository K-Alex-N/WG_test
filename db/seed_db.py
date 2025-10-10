import random
import sqlite3

from db.init_db import cursor, conn


def get_random_integer():
    """как сказано в задании, все интеджеры заполняются случайным числом от 1 до 20"""
    return random.randint(1, 20)


WEAPONS_COUNT = 20
HULLS_COUNT = 5
ENGINES_COUNT = 6
SHIPS_COUNT = 200

weapons_data = [
    (
        f"Weapon-{i + 1}",
        get_random_integer(),
        get_random_integer(),
        get_random_integer(),
        get_random_integer(),
        get_random_integer()
    )
    for i in range(WEAPONS_COUNT)
]

hulls_data = [
    (
        f"Hull-{i + 1}",
        get_random_integer(),
        get_random_integer(),
        get_random_integer()
    )
    for i in range(HULLS_COUNT)
]

engines_data = [
    (
        f"Engine-{i + 1}",
        get_random_integer(),
        get_random_integer()
    )
    for i in range(ENGINES_COUNT)
]

ships_data = [
    (
        f"Ship-{i + 1}",
        f"Weapon-{random.randint(1, WEAPONS_COUNT)}",
        f"Hull-{random.randint(1, HULLS_COUNT)}",
        f"Engine-{random.randint(1, ENGINES_COUNT)}"
    )
    for i in range(SHIPS_COUNT)
]


def seed_db():
    try:
        cursor.executemany(
            "INSERT INTO weapons VALUES (?, ?, ?, ?, ?, ?)",
            weapons_data
        )

        cursor.executemany(
            "INSERT INTO hulls VALUES (?, ?, ?, ?)",
            hulls_data)

        cursor.executemany(
            "INSERT INTO engines VALUES (?, ?, ?)",
            engines_data)

        cursor.executemany(
            "INSERT INTO ships VALUES (?, ?, ?, ?)",
            ships_data)

        conn.commit()
        # logging.info("Database populated successfully.")

    except sqlite3.Error as e:
        conn.rollback()
        # logging.info(f"Error: {e}")

    finally:
        conn.close()
