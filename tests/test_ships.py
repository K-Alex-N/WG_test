import pytest

from db.conn_db import conn_db
from config import TEMP_DB_NAME, SHIPS_COUNT, COMPONENTS_LIST, DB_NAME

import random
from dataclasses import dataclass, asdict


@dataclass
class Ship:
    ship_id: str
    weapon: str
    hull: str
    engine: str

    def __getitem__(self, item):
        return getattr(self, item)


# class WeaponData:
#
#
# class Component:

# @dataclass
# class Component:
#     name: str
#     params: list[str]
#     db_name: str

@dataclass
class Weapon:
    name: str
    reload_speed: int
    rotational_speed: int
    diameter: int
    power_volley: int
    count: int


@dataclass
class Hull:
    name: str
    armor: int
    type: int
    capacity: int


@dataclass
class Engine:
    name: str
    power: int
    type: int


def get_component_object(comp, row):
    if comp == "weapon":
        return Weapon(*row)
    elif comp == "hull":
        return Hull(*row)
    elif comp == "engine":
        return Engine(*row)
    else:
        raise Exception(f"Unknown component: {comp}")


def get_ship(db: str, ship_id: str) -> Ship:
    with conn_db(db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ships WHERE ship=?", (ship_id,))
        row = cursor.fetchone()

    if not row:
        raise ValueError(f"Ship not found: {ship_id}")
    return Ship(*row)


def get_original_ship(ship_id: str) -> Ship:
    return get_ship(DB_NAME, ship_id)


def get_changed_ship(ship_id: str) -> Ship:
    return get_ship(TEMP_DB_NAME, ship_id)


def check_comp_equality(comp: str, orig_ship: Ship, changed_ship: Ship) -> None:
    if orig_ship[comp] != changed_ship[comp]:
        pytest.fail(f"{orig_ship.ship_id}, {comp}\n\tExpected {orig_ship[comp]}, was {changed_ship[comp]}")


def check_param_equality(orig_comp, changed_comp, ship_name: str):
    orig_comp_dict = asdict(orig_comp)
    changed_comp_dict = asdict(changed_comp)

    for param, value in orig_comp_dict.items():
        if value != changed_comp_dict[param]:
            pytest.fail(f"{ship_name}, {changed_comp_dict["name"]}\n"
                        f"\t{param}: expected {value}, was {changed_comp_dict[param]}")


def get_comp(db: str, comp: str, comp_id: str) -> Weapon | Hull | Engine:
    with conn_db(db) as conn:
        cursor = conn.cursor()
        comp_db = f"{comp}s"  # избавиться от этого потом
        cursor.execute(
            f"SELECT * "
            f"FROM {comp_db} "
            f"WHERE {comp}=?",
            (comp_id,))
        row = cursor.fetchone()

    if not row:
        raise ValueError(f"Component not found: {comp_id}")
    return get_component_object(comp, row)


def get_orig_comp(comp: str, comp_id: str):
    return get_comp(DB_NAME, comp, comp_id)


def get_changed_comp(comp: str, comp_id: str):
    return get_comp(TEMP_DB_NAME, comp, comp_id)


@pytest.mark.parametrize("comp", COMPONENTS_LIST)
# @pytest.mark.parametrize("ship_id", range(1, SHIPS_COUNT + 1))  # maybe put f"Ship-{ship_id}" here
@pytest.mark.parametrize("ship_id", range(1, 10))
def test_123(comp, ship_id):
    ship_id = f"Ship-{ship_id}"

    orig_ship = get_original_ship(ship_id)
    changed_ship = get_changed_ship(ship_id)

    check_comp_equality(comp, orig_ship, changed_ship)

    comp_id = orig_ship[comp]
    orig_comp = get_orig_comp(comp, comp_id)
    changed_comp = get_changed_comp(comp, comp_id)

    check_param_equality(orig_comp, changed_comp, ship_id)

    # for param in comp.params:
    # for param in get_params(comp):
    #     check_param_equality(param, comp, ship_id)
