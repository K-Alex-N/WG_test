from dataclasses import asdict

import pytest

from config import COMPONENTS_LIST, DB_NAME, TEMP_DB_NAME
from constants import COMPARE_COMPONENTS_FAIL_MESSAGE, COMPARE_PARAMS_FAIL_MESSAGE
from db.conn_db import get_cursor
from db.models import Component, Engine, Hull, Ship, Weapon
from tests.services import ShipService, ComponentService, ComparisonService

# def get_component_obj(comp: str, row: tuple) -> Component:
#     comp_map = {"weapon": Weapon, "hull": Hull, "engine": Engine}
#     comp_class = comp_map.get(comp)
#     if comp_class is None:
#         raise ValueError(f"Unknown component: '{comp}'")
#     return comp_class(*row)
# 
# 
# def get_ship(db: str, ship_id: str) -> Ship:
#     with get_cursor(db) as cursor:
#         cursor.execute("SELECT * FROM ships WHERE ship=?", (ship_id,))
#         row = cursor.fetchone()
# 
#     if not row:
#         raise ValueError(f"Ship not found: {ship_id}")
#     return Ship(*row)
# 
# 
# def get_original_ship(ship_id: str) -> Ship:
#     return get_ship(DB_NAME, ship_id)
# 
# 
# def get_changed_ship(ship_id: str) -> Ship:
#     return get_ship(TEMP_DB_NAME, ship_id)
# 
# 
# def compare_components_in_ship(comp: str, orig_ship: Ship, changed_ship: Ship) -> None:
#     if orig_ship[comp] != changed_ship[comp]:
#         pytest.fail(
#             COMPARE_COMPONENTS_FAIL_MESSAGE.format(
#                 ship_id=orig_ship.ship_id,
#                 comp=comp,
#                 orig_comp=orig_ship[comp],
#                 changed_comp=changed_ship[comp],
#             )
#         )
# 
# 
# def compare_params_in_component(orig_comp, changed_comp, ship_id: str) -> None:
#     for param, value in asdict(orig_comp).items():
#         if value != changed_comp[param]:
#             pytest.fail(
#                 COMPARE_PARAMS_FAIL_MESSAGE.format(
#                     ship_id=ship_id,
#                     comp_id=changed_comp["comp_id"],
#                     param=param,
#                     orig_value=value,
#                     changed_value=changed_comp[param],
#                 )
#             )
# 
# 
# def get_comp(db: str, comp: str, comp_id: str) -> Component:
#     comp_table = f"{comp}s"
#     with get_cursor(db) as cursor:
#         cursor.execute(f"SELECT * FROM {comp_table} WHERE {comp}=?", (comp_id,))
#         row = cursor.fetchone()
# 
#     if not row:
#         raise ValueError(f"Component not found: {comp_id}")
#     return get_component_obj(comp, row)
# 
# 
# def get_orig_comp(comp: str, comp_id: str) -> Component:
#     return get_comp(DB_NAME, comp, comp_id)
# 
# 
# def get_changed_comp(comp: str, comp_id: str) -> Component:
#     return get_comp(TEMP_DB_NAME, comp, comp_id)


ship_service = ShipService()
component_service = ComponentService()
comparison_service = ComparisonService()

@pytest.mark.parametrize("comp", COMPONENTS_LIST)
# @pytest.mark.parametrize("i", range(1, SHIPS_COUNT + 1))
@pytest.mark.parametrize("i", range(1, 5))
def test_differences_in_databases(comp: str, i: int) -> None:
    """1. Check if the gun, hull, or engine of the ship has changed.
    2. Check if the value of a component parameter has changed.
    """
    ship_id = f"Ship-{i}"
    # logger.debug(f"Testing differences for {ship_id}, component: {comp}")

    # compare components in ship
    orig_ship = ship_service.get_original_ship(ship_id)
    changed_ship = ship_service.get_changed_ship(ship_id)

    comparison_service.compare_ship_components(comp, orig_ship, changed_ship)

    # compare parameters in component
    comp_id = orig_ship[comp]
    orig_comp = component_service.get_original_component(comp, comp_id)
    changed_comp = component_service.get_changed_component(comp, comp_id)

    comparison_service.compare_component_parameters(orig_comp, changed_comp, ship_id)
