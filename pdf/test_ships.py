import sqlite3
import pytest

def get_ship_data(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    ships = {}
    for row in c.execute("SELECT * FROM ships"):
        ship, weapon, hull, engine = row
        ships[ship] = {"weapon": weapon, "hull": hull, "engine": engine}
    conn.close()
    return ships

def get_component_data(db_path, table, key):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    data = {}
    for row in c.execute(f"SELECT * FROM {table}"):
        data[row[0]] = row[1:]
    conn.close()
    return data

original_db = "ships.db"

@pytest.mark.parametrize("ship_id", range(1, 2))
def test_weapon(randomized_db, ship_id):
    ship_name = f"ship-{ship_id}"
    orig_ships = get_ship_data(original_db)
    rand_ships = get_ship_data(randomized_db)

    orig_weapon = orig_ships[ship_name]["weapon"]
    rand_weapon = rand_ships[ship_name]["weapon"]

    if orig_weapon != rand_weapon:
        print(orig_weapon)
        print(rand_weapon)
        pytest.fail(f"{ship_name}, {rand_weapon}\nexpected {orig_weapon}, was {rand_weapon}")

    orig_data = get_component_data(original_db, "weapons", orig_weapon)[orig_weapon]
    rand_data = get_component_data(randomized_db, "weapons", rand_weapon)[rand_weapon]

    for i, param in enumerate(["reload_speed", "rotational_speed", "diameter", "power_volley", "count"]):
        if orig_data[i] != rand_data[i]:
            pytest.fail(f"{ship_name}, {rand_weapon}\n{param}: expected {orig_data[i]}, was {rand_data[i]}")

# @pytest.mark.parametrize("ship_id", range(1, 201))
# def test_hull(randomized_db, ship_id):
#     # аналогично test_weapon, но для hulls
#     ...
#
# @pytest.mark.parametrize("ship_id", range(1, 201))
# def test_engine(randomized_db, ship_id):
#     # аналогично test_weapon, но для engines
#     ...
