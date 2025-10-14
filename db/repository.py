

from constants import (
    REPO_COMPONENT_FIND_ALL,
    REPO_COMPONENT_FIND_ALL_SUCCESS,
    REPO_COMPONENT_FIND_NOT_FOUND,
    REPO_COMPONENT_FIND_START,
    REPO_COMPONENT_FIND_SUCCESS,
    REPO_COMPONENT_UPDATE,
    REPO_COMPONENT_UPDATE_SUCCESS,
    REPO_SHIP_FIND_ALL,
    REPO_SHIP_FIND_ALL_SUCCESS,
    REPO_SHIP_FIND_NOT_FOUND,
    REPO_SHIP_FIND_START,
    REPO_SHIP_FIND_SUCCESS,
    REPO_SHIP_UPDATE,
    REPO_SHIP_UPDATE_SUCCESS,
)
from db.conn_db import get_cursor
from db.logger import logger


class ShipRepository:

    @staticmethod
    def find_by_id(db_name: str, ship_id: str) -> tuple | None:

        logger.debug(REPO_SHIP_FIND_START.format(ship_id=ship_id, db_name=db_name))
        with get_cursor(db_name) as cursor:
            cursor.execute("SELECT * FROM ships WHERE ship=?", (ship_id,))
            ship = cursor.fetchone()

        if ship:
            logger.debug(REPO_SHIP_FIND_SUCCESS.format(ship_id=ship_id))
        else:
            logger.debug(
                REPO_SHIP_FIND_NOT_FOUND.format(ship_id=ship_id, db_name=db_name))

        return ship

    @staticmethod
    def find_all(db_name: str) -> list[tuple]:

        logger.debug(REPO_SHIP_FIND_ALL.format(db_name=db_name))
        with get_cursor(db_name) as cursor:
            ships = cursor.execute("SELECT * FROM ships").fetchall()

        logger.debug(
            REPO_SHIP_FIND_ALL_SUCCESS.format(count=len(ships), db_name=db_name))
        return ships

    @staticmethod
    def update_component(db_name: str, ship_id: str, component: str,
                         component_id: str) -> None:

        logger.debug(REPO_SHIP_UPDATE.format(
            ship_id=ship_id,
            component=component,
            component_id=component_id,
            db_name=db_name
        ))
        with get_cursor(db_name) as cursor:
            cursor.execute(
                f"UPDATE ships SET {component} = ? WHERE ship = ?",
                (component_id, ship_id),
            )

        logger.debug(REPO_SHIP_UPDATE_SUCCESS.format(ship_id=ship_id))


class ComponentRepository:

    @staticmethod
    def find_by_id(db_name: str, component_table: str, component_type: str,
                   component_id: str) -> tuple | None:

        logger.debug(REPO_COMPONENT_FIND_START.format(
            component_type=component_type,
            component_id=component_id,
            db_name=db_name
        ))
        with get_cursor(db_name) as cursor:
            cursor.execute(
                f"SELECT * FROM {component_table} WHERE {component_type}=?",
                (component_id,)
            )
            component = cursor.fetchone()

        if component:
            logger.debug(REPO_COMPONENT_FIND_SUCCESS.format(component_id=component_id))
        else:
            logger.debug(REPO_COMPONENT_FIND_NOT_FOUND.format(
                component_id=component_id,
                db_name=db_name
            ))

        return component

    @staticmethod
    def find_all(db_name: str, component_table: str) -> list[tuple]:

        logger.debug(REPO_COMPONENT_FIND_ALL.format(
            component_table=component_table,
            db_name=db_name
        ))
        with get_cursor(db_name) as cursor:
            components = cursor.execute(f"SELECT * FROM {component_table}").fetchall()

        logger.debug(REPO_COMPONENT_FIND_ALL_SUCCESS.format(
            count=len(components),
            component_table=component_table
        ))
        return components

    @staticmethod
    def update_parameter(
            db_name: str,
            component_table: str,
            component_type: str,
            component_id: str,
            param_name: str,
            param_value: int
    ) -> None:

        logger.debug(REPO_COMPONENT_UPDATE.format(
            component_id=component_id,
            param_name=param_name,
            param_value=param_value
        ))
        with get_cursor(db_name) as cursor:
            cursor.execute(
                f"UPDATE {component_table} SET {param_name} = ? WHERE {component_type} = ?",
                (param_value, component_id),
            )

        logger.debug(REPO_COMPONENT_UPDATE_SUCCESS.format(component_id=component_id))

