from db.conn_db import get_cursor
from db.tmp_db import drop_db_if_exists


def create_db() -> None:
    drop_db_if_exists()

    weapons_table = """
        CREATE TABLE IF NOT EXISTS weapons (
            weapon TEXT PRIMARY KEY,
            reload_speed INTEGER,
            rotational_speed INTEGER,
            diameter INTEGER,
            power_volley INTEGER,
            count INTEGER
        );
    """

    hulls_table = """
        CREATE TABLE IF NOT EXISTS hulls (
            hull TEXT PRIMARY KEY,
            armor INTEGER,
            type INTEGER,
            capacity INTEGER
        );
    """

    engines_table = """
        CREATE TABLE IF NOT EXISTS engines (
            engine TEXT PRIMARY KEY,
            power INTEGER,
            type INTEGER
        );
    """

    ships_table = """
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

    # создать общий класс для всех таблиц
    # затем, код ниже пропустить церез цикл

    # logger.info(f"Creating database: {db_name}")
    # drop_db_if_exists(db_name)

    with get_cursor() as cursor:
        # for table_sql in DatabaseSchema.get_all_tables():
        #     logger.debug(f"Creating table with SQL: {table_sql.strip()}")
        #     cursor.execute(table_sql)

        cursor.execute(weapons_table)
        cursor.execute(hulls_table)
        cursor.execute(engines_table)
        cursor.execute(ships_table)

    # logger.info(f"Database {db_name} created successfully with all tables and indexes")
    # logging.info("Databases created successfully.")
