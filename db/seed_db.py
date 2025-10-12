import random

from config import ENGINES_COUNT, HULLS_COUNT, SHIPS_COUNT, WEAPONS_COUNT
from db.conn_db import get_cursor
from db.utils import get_random_integer

weapons_data = [
    (
        f"Weapon-{i + 1}",
        get_random_integer(),
        get_random_integer(),
        get_random_integer(),
        get_random_integer(),
        get_random_integer(),
    )
    for i in range(WEAPONS_COUNT)
]
# fmt: off
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
# fmt: on
ships_data = [
    (
        f"Ship-{i + 1}",
        f"Weapon-{random.randint(1, WEAPONS_COUNT)}",
        f"Hull-{random.randint(1, HULLS_COUNT)}",
        f"Engine-{random.randint(1, ENGINES_COUNT)}",
    )
    for i in range(SHIPS_COUNT)
]


def seed_db():
    with get_cursor() as cursor:
        cursor.executemany(
            "INSERT INTO weapons VALUES (?, ?, ?, ?, ?, ?)", weapons_data
        )
        cursor.executemany("INSERT INTO hulls VALUES (?, ?, ?, ?)", hulls_data)
        cursor.executemany("INSERT INTO engines VALUES (?, ?, ?)", engines_data)
        cursor.executemany("INSERT INTO ships VALUES (?, ?, ?, ?)", ships_data)

    # logging.info("Database populated successfully.")
