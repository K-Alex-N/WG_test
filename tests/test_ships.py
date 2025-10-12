from dataclasses import asdict
from typing import Any

import pytest

from config import COMPONENTS_LIST, DB_NAME, TEMP_DB_NAME
from db.conn_db import get_cursor
from db.models import Engine, Hull, Ship, Weapon, Component


def get_component_object(component: str, db_row: tuple) -> Component:
    component_class = {"weapon": Weapon, "hull": Hull, "engine": Engine}[component]
    if component_class is None:
        raise ValueError(f"Unknown component: '{component}'")
    return component_class(*db_row)


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


def compare_components_in_ship(
    component: str, orig_ship: Ship, changed_ship: Ship
) -> None:
    if orig_ship[component] != changed_ship[component]:
        pytest.fail(
            f"{orig_ship.ship_id}, {component}\n"
            f"\tExpected {orig_ship[component]}, was {changed_ship[component]}"
        )


def compare_params_in_component(
    orig_component, changed_component, ship_id: str
) -> None:
    orig_component_dict = asdict(orig_component)
    changed_component_dict = asdict(changed_component)

    for param, value in orig_component_dict.items():
        if value != changed_component_dict[param]:
            pytest.fail(
                f"{ship_id}, {changed_component_dict['component_id']}\n"
                f"\t{param}: expected {value}, was {changed_component_dict[param]}"
            )


def get_component(db: str, component: str, component_id: str) -> Component:
    component_db = f"{component}s"
    with get_cursor(db) as cursor:
        cursor.execute(
            f"SELECT * FROM {component_db} WHERE {component}=?", (component_id,)
        )
        row = cursor.fetchone()

    if not row:
        raise ValueError(f"Component not found: {component_id}")
    return get_component_object(component, row)


def get_orig_component(component: str, component_id: str) -> Component:
    return get_component(DB_NAME, component, component_id)


def get_changed_component(component: str, component_id: str) -> Component:
    return get_component(TEMP_DB_NAME, component, component_id)


@pytest.mark.parametrize("component", COMPONENTS_LIST)
# @pytest.mark.parametrize("i", range(1, SHIPS_COUNT + 1))
@pytest.mark.parametrize("i", range(1, 5))
def test_differences_in_databases(component, i):
    """
    TASK
    1. Check if the gun, hull, or engine of the ship has changed.
    2. Check if the value of a component parameter does not match what it was before
    the randomizer was run.
    """
    ship_id = f"Ship-{i}"

    # compare components in ship
    orig_ship = get_original_ship(ship_id)
    changed_ship = get_changed_ship(ship_id)

    compare_components_in_ship(component, orig_ship, changed_ship)

    # compare parameters in component
    component_id = orig_ship[component]
    orig_component = get_orig_component(component, component_id)
    changed_component = get_changed_component(component, component_id)

    compare_params_in_component(orig_component, changed_component, ship_id)
