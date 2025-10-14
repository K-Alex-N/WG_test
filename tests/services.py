
import pytest

from config import (
    DB_NAME,
    ENGINES_COUNT,
    HULLS_COUNT,
    TEMP_DB_NAME,
    WEAPONS_COUNT,
)
from constants import (
    COMPARE_COMPONENTS_FAIL_MESSAGE,
    COMPARE_PARAMS_FAIL_MESSAGE,
    COMPONENT_NOT_FOUND_MESSAGE,
    SERVICE_COMPARE_PARAMS_DIFFER,
    SERVICE_COMPARE_PARAMS_START,
    SERVICE_COMPARE_SHIPS_DIFFER,
    SERVICE_COMPARE_SHIPS_MATCH,
    SERVICE_COMPARE_SHIPS_START,
    SERVICE_GET_COMPONENT_ERROR,
    SERVICE_GET_COMPONENT_START,
    SERVICE_GET_COMPONENT_SUCCESS,
    SERVICE_GET_SHIP_ERROR,
    SERVICE_GET_SHIP_START,
    SERVICE_GET_SHIP_SUCCESS,
    SERVICE_UPDATE_COMPONENT,
    SERVICE_UPDATE_SHIP,
    SHIP_NOT_FOUND_MESSAGE,
    UNKNOWN_COMPONENT_MESSAGE,
)
from db.logger import logger
from db.models import Component, Engine, Hull, Ship, Weapon
from db.repository import ComponentRepository, ShipRepository


class ComponentMapper:
    COMPONENT_CLASSES = {
        "weapon": Weapon,
        "hull": Hull,
        "engine": Engine,
    }

    COMPONENT_COUNTS = {
        "weapon": WEAPONS_COUNT,
        "hull": HULLS_COUNT,
        "engine": ENGINES_COUNT,
    }

    @classmethod
    def get_component_class(cls, component_type: str) -> type[Component]:
        comp_class = cls.COMPONENT_CLASSES.get(component_type)
        if comp_class is None:
            raise ValueError(UNKNOWN_COMPONENT_MESSAGE.format(comp=component_type))
        return comp_class

    @classmethod
    def get_component_count(cls, component_type: str) -> int:
        count = cls.COMPONENT_COUNTS.get(component_type)
        if count is None:
            raise ValueError(UNKNOWN_COMPONENT_MESSAGE.format(comp=component_type))
        return count

    @classmethod
    def create_comp_instance_from_row(cls, comp_type: str, row: tuple) -> Component:
        comp_class = cls.get_component_class(comp_type)
        return comp_class(*row)


class ShipService:
    def __init__(self, repository: ShipRepository | None = None):
        self.repository = repository or ShipRepository()

    def get_ship(self, db_name: str, ship_id: str) -> Ship:
        logger.info(SERVICE_GET_SHIP_START.format(ship_id=ship_id, db_name=db_name))
        try:
            row = self.repository.find_by_id(db_name, ship_id)
            if not row:
                error_msg = SHIP_NOT_FOUND_MESSAGE.format(ship_id=ship_id)
                logger.error(
                    SERVICE_GET_SHIP_ERROR.format(ship_id=ship_id, error=error_msg)
                )
                raise ValueError(error_msg)

            ship = Ship(*row)
            logger.info(SERVICE_GET_SHIP_SUCCESS.format(ship_id=ship_id))
            return ship
        except Exception as e:
            logger.error(SERVICE_GET_SHIP_ERROR.format(ship_id=ship_id, error=str(e)))
            raise

    def get_original_ship(self, ship_id: str) -> Ship:
        return self.get_ship(DB_NAME, ship_id)

    def get_changed_ship(self, ship_id: str) -> Ship:
        return self.get_ship(TEMP_DB_NAME, ship_id)

    def get_all_ships(self, db_name: str) -> list[tuple]:
        return self.repository.find_all(db_name)

    def update_ship_component(
        self, db_name: str, ship_id: str, component_type: str, component_id: str
    ) -> None:
        logger.info(
            SERVICE_UPDATE_SHIP.format(
                ship_id=ship_id,
                component_type=component_type,
                component_id=component_id,
            )
        )
        self.repository.update_component(db_name, ship_id, component_type, component_id)


class ComponentService:
    def __init__(self, repository: ComponentRepository | None = None):
        self.repository = repository or ComponentRepository()

    def get_component(
        self, db_name: str, component_type: str, component_id: str
    ) -> Component:
        logger.info(
            SERVICE_GET_COMPONENT_START.format(
                component_type=component_type,
                component_id=component_id,
                db_name=db_name,
            )
        )
        try:
            component_table = f"{component_type}s"
            row = self.repository.find_by_id(
                db_name, component_table, component_type, component_id
            )
            if not row:
                error_msg = COMPONENT_NOT_FOUND_MESSAGE.format(comp_id=component_id)
                logger.error(
                    SERVICE_GET_COMPONENT_ERROR.format(
                        component_id=component_id, error=error_msg
                    )
                )
                raise ValueError(error_msg)

            component = ComponentMapper.create_comp_instance_from_row(
                component_type, row
            )
            logger.info(SERVICE_GET_COMPONENT_SUCCESS.format(component_id=component_id))
            return component
        except Exception as e:
            logger.error(
                SERVICE_GET_COMPONENT_ERROR.format(
                    component_id=component_id, error=str(e)
                )
            )
            raise

    def get_original_component(
        self, component_type: str, component_id: str
    ) -> Component:
        return self.get_component(DB_NAME, component_type, component_id)

    def get_changed_component(
        self, component_type: str, component_id: str
    ) -> Component:
        return self.get_component(TEMP_DB_NAME, component_type, component_id)

    def get_all_components(self, db_name: str, component_table: str) -> list[tuple]:
        return self.repository.find_all(db_name, component_table)

    def update_component_parameter(
        self,
        db_name: str,
        component_type: str,
        component_id: str,
        param_name: str,
        param_value: int,
    ) -> None:
        logger.info(
            SERVICE_UPDATE_COMPONENT.format(
                component_id=component_id, param_name=param_name
            )
        )
        component_table = f"{component_type}s"
        self.repository.update_parameter(
            db_name,
            component_table,
            component_type,
            component_id,
            param_name,
            param_value,
        )


class ComparisonService:
    @staticmethod
    def compare_ship_components(
        component_type: str, original_ship: Ship, changed_ship: Ship
    ) -> None:
        logger.debug(SERVICE_COMPARE_SHIPS_START.format(component_type=component_type))

        orig_comp_id = original_ship[component_type]
        changed_comp_id = changed_ship[component_type]

        if orig_comp_id != changed_comp_id:
            logger.info(
                SERVICE_COMPARE_SHIPS_DIFFER.format(
                    component_type=component_type,
                    orig=orig_comp_id,
                    changed=changed_comp_id,
                )
            )
            pytest.fail(
                COMPARE_COMPONENTS_FAIL_MESSAGE.format(
                    ship_id=original_ship.ship_id,
                    comp=component_type,
                    orig_comp=orig_comp_id,
                    changed_comp=changed_comp_id,
                )
            )
        else:
            logger.debug(
                SERVICE_COMPARE_SHIPS_MATCH.format(
                    component_type=component_type, component_id=orig_comp_id
                )
            )

    @staticmethod
    def compare_component_params(
        original_component: Component, changed_component: Component, ship_id: str
    ) -> None:
        comp_id = changed_component["comp_id"]
        logger.debug(SERVICE_COMPARE_PARAMS_START.format(component_id=comp_id))

        for param, value in vars(original_component).items():
            if value != changed_component[param]:
                logger.info(
                    SERVICE_COMPARE_PARAMS_DIFFER.format(
                        param=param,
                        orig_value=value,
                        changed_value=changed_component[param],
                    )
                )
                pytest.fail(
                    COMPARE_PARAMS_FAIL_MESSAGE.format(
                        ship_id=ship_id,
                        comp_id=comp_id,
                        param=param,
                        orig_value=value,
                        changed_value=changed_component[param],
                    )
                )


ship_service = ShipService()
component_service = ComponentService()
comparison_service = ComparisonService()
