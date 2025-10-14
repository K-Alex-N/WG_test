import pytest

from config import COMPONENTS, SHIPS_COUNT
from constants import COMPARE_COMPONENTS_IN_SHIP, COMPARE_PARAMS_IN_COMPONENT
from db.logger import logger
from tests.services import ship_service, comparison_service, component_service


@pytest.mark.parametrize("component_type", COMPONENTS)
# @pytest.mark.parametrize("i", range(1, SHIPS_COUNT + 1))
@pytest.mark.parametrize("i", range(1, 5))
def test_differences_in_databases(component_type, i: int, randomize_tmp_db) -> None:
    """1. Check if the gun, hull, or engine of the ship has changed.
    2. Check if the value of a component parameter has changed.
    """
    ship_id = f"Ship-{i}"

    # Compare components in ship
    logger.debug(COMPARE_COMPONENTS_IN_SHIP.format(ship_id=ship_id))

    original_ship = ship_service.get_original_ship(ship_id)
    changed_ship = ship_service.get_changed_ship(ship_id)
    comparison_service.compare_ship_components(component_type, original_ship,
                                               changed_ship)

    # Compare parameters in component
    logger.debug(COMPARE_PARAMS_IN_COMPONENT.format(component_type=component_type))

    component_id = original_ship[component_type]
    original_component = component_service.get_original_component(component_type,
                                                                  component_id)
    changed_component = component_service.get_changed_component(component_type,
                                                                component_id)
    comparison_service.compare_component_params(original_component,
                                                changed_component,
                                                ship_id)
