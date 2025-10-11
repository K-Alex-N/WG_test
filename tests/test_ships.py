from dataclasses import asdict

import pytest

from config import COMPONENTS_LIST, DB_NAME, TEMP_DB_NAME
from db.conn_db import get_cursor
from db.models import Engine, Hull, Ship, Weapon


def get_component_object(comp: str, row: tuple) -> Weapon | Hull | Engine:
    comp_map = {
        "weapon": Weapon,
        "hull": Hull,
        "engine": Engine,
    }
    comp_class = comp_map[comp]
    return comp_class(*row)


def get_ship(db: str, ship_id: str) -> Ship:
    with get_cursor(db) as cursor:
        cursor.execute("SELECT * FROM ships WHERE ship=?", (ship_id,))
        row = cursor.fetchone()

    if not row:
        raise ValueError(f"Ship not found: {ship_id}")
    return Ship(*row)


def get_original_ship(ship_id: str) -> Ship:
    return get_ship(DB_NAME, ship_id)


def get_changed_ship(ship_id: str) -> Ship:
    return get_ship(TEMP_DB_NAME, ship_id)


def compare_components_in_ship(comp: str, orig_ship: Ship, changed_ship: Ship) -> None:
    if orig_ship[comp] != changed_ship[comp]:
        pytest.fail(
            f"{orig_ship.ship_id}, {comp}\n"
            f"\tExpected {orig_ship[comp]}, was {changed_ship[comp]}"
        )


def compare_params_in_component(orig_comp, changed_comp, ship_id: str) -> None:
    orig_comp_dict = asdict(orig_comp)
    changed_comp_dict = asdict(changed_comp)

    for param, value in orig_comp_dict.items():
        if value != changed_comp_dict[param]:
            pytest.fail(
                f"{ship_id}, {changed_comp_dict['comp_id']}\n"
                f"\t{param}: expected {value}, was {changed_comp_dict[param]}"
            )


def get_comp(db: str, comp: str, comp_id: str) -> Weapon | Hull | Engine:
    comp_db = f"{comp}s"
    with get_cursor(db) as cursor:
        cursor.execute(f"SELECT * FROM {comp_db} WHERE {comp}=?", (comp_id,))
        row = cursor.fetchone()

    if not row:
        raise ValueError(f"Component not found: {comp_id}")
    return get_component_object(comp, row)


def get_orig_comp(comp: str, comp_id: str) -> Weapon | Hull | Engine:
    return get_comp(DB_NAME, comp, comp_id)


def get_changed_comp(comp: str, comp_id: str) -> Weapon | Hull | Engine:
    return get_comp(TEMP_DB_NAME, comp, comp_id)


@pytest.mark.parametrize("comp", COMPONENTS_LIST)
@pytest.mark.parametrize("i", range(1, 5))
def test_differences_in_databases(comp, i):
    ship_id = f"Ship-{i}"

    # compare name of component in ship
    orig_ship = get_original_ship(ship_id)
    changed_ship = get_changed_ship(ship_id)

    compare_components_in_ship(comp, orig_ship, changed_ship)

    # compare values of parameters in component
    comp_id = orig_ship[comp]
    orig_comp = get_orig_comp(comp, comp_id)
    changed_comp = get_changed_comp(comp, comp_id)

    compare_params_in_component(orig_comp, changed_comp, ship_id)
