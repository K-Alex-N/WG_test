"""Utility functions for database operations."""

import random
from typing import List, Tuple

from config import MAX_PARAM_VALUE, MIN_PARAM_VALUE
from db.logger import logger


def get_int_from_1_to_20() -> int:
    """
    Generate a random integer between 1 and 20.
    
    As specified in the task, all parameters are filled with random numbers from 1 to 20.
    
    Returns:
        Random integer between 1 and 20 (inclusive)
    """
    return random.randint(MIN_PARAM_VALUE, MAX_PARAM_VALUE)


def validate_parameter_value(value: int) -> bool:
    """
    Validate that a parameter value is within the allowed range.
    
    Args:
        value: The value to validate
        
    Returns:
        True if value is valid, False otherwise
    """
    return MIN_PARAM_VALUE <= value <= MAX_PARAM_VALUE


def generate_component_data(
    component_type: str, 
    count: int, 
    param_count: int
) -> List[Tuple[str, ...]]:
    """
    Generate random data for a component type.
    
    Args:
        component_type: Type of component (weapon, hull, engine)
        count: Number of components to generate
        param_count: Number of parameters per component
        
    Returns:
        List of tuples containing component data
    """
    data = []
    for i in range(count):
        component_id = f"{component_type.capitalize()}-{i + 1}"
        params = [get_int_from_1_to_20() for _ in range(param_count)]
        data.append((component_id, *params))
    
    logger.debug(f"Generated {count} {component_type} components")
    return data


def generate_ship_data(
    ship_count: int,
    weapon_count: int,
    hull_count: int,
    engine_count: int
) -> List[Tuple[str, str, str, str]]:
    """
    Generate random ship data with component assignments.
    
    Args:
        ship_count: Number of ships to generate
        weapon_count: Number of available weapons
        hull_count: Number of available hulls
        engine_count: Number of available engines
        
    Returns:
        List of tuples containing ship data
    """
    data = []
    for i in range(ship_count):
        ship_id = f"Ship-{i + 1}"
        weapon = f"Weapon-{random.randint(1, weapon_count)}"
        hull = f"Hull-{random.randint(1, hull_count)}"
        engine = f"Engine-{random.randint(1, engine_count)}"
        data.append((ship_id, weapon, hull, engine))
    
    logger.debug(f"Generated {ship_count} ships")
    return data


def get_random_component_id(component_type: str, max_count: int) -> str:
    """
    Get a random component ID for the specified type.
    
    Args:
        component_type: Type of component (weapon, hull, engine)
        max_count: Maximum number of components of this type
        
    Returns:
        Random component ID string
    """
    component_id = random.randint(1, max_count)
    return f"{component_type.capitalize()}-{component_id}"


def get_random_parameter_value() -> int:
    """
    Get a random parameter value within the allowed range.
    
    Returns:
        Random integer between MIN_PARAM_VALUE and MAX_PARAM_VALUE
    """
    return get_int_from_1_to_20()
