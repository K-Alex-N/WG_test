import random
import shutil
import os

from db.init_db import DB_NAME, init_db, cursor

TEMP_DB_NAME = "temp_" + DB_NAME


def create_copy_db():
    if os.path.exists(TEMP_DB_NAME):
        os.remove(TEMP_DB_NAME)
    shutil.copy(DB_NAME, TEMP_DB_NAME)


def init_copy_db():
    init_db(TEMP_DB_NAME)


def randomize_ships():
    # TODO достать все карабли из БД
    # cursor.

    cursor.execute("SELECT * FROM ships")
    ships = cursor.fetchall()

    # pytest.fail(e) использовать

    # может быть создать ДАТАКЛАССЫ или МОДЕЛЬКИ для каждой БД.
    # ЧТОБЫ потом через точку доставать нужный параметр!!!!
    #
    # можно валидацию через Пайдентик сделать


    for ship_data in ships:
        component = random.choice(["weapon", "hull", "engine"])


        pass


def randomize_components():
    # randomize hulls
    # randomize hulls
    # randomize hulls
    pass


def create_modified_db():
    create_copy_db()
    init_copy_db()

    randomize_ships()
    randomize_components()

    pass
