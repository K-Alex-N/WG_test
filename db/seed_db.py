import random

from config import ENGINES_COUNT, HULLS_COUNT, SHIPS_COUNT, WEAPONS_COUNT
from db.conn_db import get_cursor
from db.utils import get_int_from_1_to_20

NUM_WEAPON_PARAMS = 5
NUM_HULL_PARAMS = 3
NUM_ENGINE_PARAMS = 2


weapons_data = [
    (f"Weapon-{i + 1}", *[get_int_from_1_to_20() for _ in range(NUM_WEAPON_PARAMS)])
    for i in range(WEAPONS_COUNT)
]

hulls_data = [
    (f"Hull-{i + 1}", *[get_int_from_1_to_20() for _ in range(NUM_HULL_PARAMS)])
    for i in range(HULLS_COUNT)
]

engines_data = [
    (f"Engine-{i + 1}", *[get_int_from_1_to_20() for _ in range(NUM_ENGINE_PARAMS)])
    for i in range(ENGINES_COUNT)
]

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
