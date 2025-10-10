import pytest
import sqlite3
import shutil
import os
import random

from .create_db import create_database
from .populate_db import populate_database

@pytest.fixture(scope="session", autouse=True)
def setup_original_db():
    db_path = "ships.db"
    if not os.path.exists(db_path):
        create_database(db_path)
        populate_database(db_path)

@pytest.fixture(scope="session")
def randomized_db(tmp_path_factory):
    orig_db = "ships.db"
    temp_db = tmp_path_factory.mktemp("data") / "randomized.db"
    shutil.copy(orig_db, temp_db)

    conn = sqlite3.connect(temp_db)
    c = conn.cursor()

    for row in c.execute("SELECT ship, weapon, hull, engine FROM ships").fetchall():
        ship, weapon, hull, engine = row
        component = random.choice(["weapon", "hull", "engine"])
        new_component = None

        if component == "weapon":
            new_component = f"weapon-{random.randint(1, 20)}"
            param = random.choice(["reload_speed", "rotational_speed", "diameter", "power_volley", "count"])
            c.execute(f"UPDATE weapons SET {param} = ? WHERE weapon = ?", (random.randint(1, 20), new_component))
        elif component == "hull":
            new_component = f"hull-{random.randint(1, 5)}"
            param = random.choice(["armor", "type", "capacity"])
            c.execute(f"UPDATE hulls SET {param} = ? WHERE hull = ?", (random.randint(1, 20), new_component))
        else:
            new_component = f"engine-{random.randint(1, 6)}"
            param = random.choice(["power", "type"])
            c.execute(f"UPDATE engines SET {param} = ? WHERE engine = ?", (random.randint(1, 20), new_component))

        c.execute(f"UPDATE ships SET {component} = ? WHERE ship = ?", (new_component, ship))

    conn.commit()

    yield str(temp_db)
    # yield str(temp_db)
    conn.close()  # зачем закрывать соединение
    # удалить файл временной БД
