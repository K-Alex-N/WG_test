from db.conn_db import get_cursor
from db.tmp_db import drop_db_if_exists

weapons = """
        CREATE TABLE IF NOT EXISTS weapons (
            weapon TEXT PRIMARY KEY,
            reload_speed INTEGER,
            rotational_speed INTEGER,
            diameter INTEGER,
            power_volley INTEGER,
            count INTEGER
        );
    """

hulls = """
        CREATE TABLE IF NOT EXISTS hulls (
            hull TEXT PRIMARY KEY,
            armor INTEGER,
            type INTEGER,
            capacity INTEGER
        );
    """

engines = """
        CREATE TABLE IF NOT EXISTS engines (
            engine TEXT PRIMARY KEY,
            power INTEGER,
            type INTEGER
        );
    """

ships = """
        CREATE TABLE IF NOT EXISTS ships (
            ship TEXT PRIMARY KEY,
            weapon TEXT,
            hull TEXT,
            engine TEXT,
            FOREIGN KEY (weapon) REFERENCES weapons(weapon),
            FOREIGN KEY (hull) REFERENCES hulls(hull),
            FOREIGN KEY (engine) REFERENCES engines(engine)
        );
    """

tables = [weapons, hulls, engines, ships]


def create_db() -> None:
    drop_db_if_exists()

    with get_cursor() as cursor:
        for table in tables:
            cursor.execute(table)
            # logger.info(f"Table {table} created successfully")
