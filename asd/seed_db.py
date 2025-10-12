"""Database seeding with improved data generation and validation."""

from typing import List, Tuple

from config import (
    ENGINES_COUNT,
    HULLS_COUNT,
    SHIPS_COUNT,
    WEAPONS_COUNT,
    DB_NAME
)
from db.conn_db import DatabaseError, get_cursor
from db.logger import logger
from db.utils import (
    generate_component_data,
    generate_ship_data,
    validate_parameter_value
)


class DatabaseSeeder:
    """Handles database seeding operations."""
    
    # Parameter counts for each component type
    NUM_WEAPON_PARAMS = 5
    NUM_HULL_PARAMS = 3
    NUM_ENGINE_PARAMS = 2
    
    def __init__(self):
        self.weapons_data: List[Tuple[str, ...]] = []
        self.hulls_data: List[Tuple[str, ...]] = []
        self.engines_data: List[Tuple[str, ...]] = []
        self.ships_data: List[Tuple[str, str, str, str]] = []
    
    def generate_weapons_data(self) -> None:
        """Generate weapons data."""
        self.weapons_data = generate_component_data(
            "weapon", WEAPONS_COUNT, self.NUM_WEAPON_PARAMS
        )
        logger.info(f"Generated {len(self.weapons_data)} weapons")
    
    def generate_hulls_data(self) -> None:
        """Generate hulls data."""
        self.hulls_data = generate_component_data(
            "hull", HULLS_COUNT, self.NUM_HULL_PARAMS
        )
        logger.info(f"Generated {len(self.hulls_data)} hulls")
    
    def generate_engines_data(self) -> None:
        """Generate engines data."""
        self.engines_data = generate_component_data(
            "engine", ENGINES_COUNT, self.NUM_ENGINE_PARAMS
        )
        logger.info(f"Generated {len(self.engines_data)} engines")
    
    def generate_ships_data(self) -> None:
        """Generate ships data."""
        self.ships_data = generate_ship_data(
            SHIPS_COUNT, WEAPONS_COUNT, HULLS_COUNT, ENGINES_COUNT
        )
        logger.info(f"Generated {len(self.ships_data)} ships")
    
    def validate_data(self) -> bool:
        """
        Validate all generated data.
        
        Returns:
            True if all data is valid, False otherwise
        """
        try:
            # Validate weapons data
            for weapon in self.weapons_data:
                for param in weapon[1:]:  # Skip the weapon ID
                    if not validate_parameter_value(param):
                        logger.error(f"Invalid weapon parameter: {param}")
                        return False
            
            # Validate hulls data
            for hull in self.hulls_data:
                for param in hull[1:]:  # Skip the hull ID
                    if not validate_parameter_value(param):
                        logger.error(f"Invalid hull parameter: {param}")
                        return False
            
            # Validate engines data
            for engine in self.engines_data:
                for param in engine[1:]:  # Skip the engine ID
                    if not validate_parameter_value(param):
                        logger.error(f"Invalid engine parameter: {param}")
                        return False
            
            logger.info("All data validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Data validation failed: {e}")
            return False
    
    def seed_database(self, db_name: str = DB_NAME) -> None:
        """
        Seed the database with generated data.
        
        Args:
            db_name: Name of the database to seed
            
        Raises:
            DatabaseError: If seeding fails
        """
        try:
            logger.info(f"Starting database seeding for {db_name}")
            
            # Generate all data
            self.generate_weapons_data()
            self.generate_hulls_data()
            self.generate_engines_data()
            self.generate_ships_data()
            
            # Validate data before inserting
            if not self.validate_data():
                raise DatabaseError("Data validation failed")
            
            # Insert data into database
            with get_cursor(db_name) as cursor:
                # Insert weapons
                cursor.executemany(
                    "INSERT INTO weapons VALUES (?, ?, ?, ?, ?, ?)", 
                    self.weapons_data
                )
                logger.debug(f"Inserted {len(self.weapons_data)} weapons")
                
                # Insert hulls
                cursor.executemany(
                    "INSERT INTO hulls VALUES (?, ?, ?, ?)", 
                    self.hulls_data
                )
                logger.debug(f"Inserted {len(self.hulls_data)} hulls")
                
                # Insert engines
                cursor.executemany(
                    "INSERT INTO engines VALUES (?, ?, ?)", 
                    self.engines_data
                )
                logger.debug(f"Inserted {len(self.engines_data)} engines")
                
                # Insert ships
                cursor.executemany(
                    "INSERT INTO ships VALUES (?, ?, ?, ?)", 
                    self.ships_data
                )
                logger.debug(f"Inserted {len(self.ships_data)} ships")
            
            logger.info(f"Database {db_name} seeded successfully with all data")
            
        except Exception as e:
            logger.error(f"Database seeding failed for {db_name}: {e}")
            raise DatabaseError(f"Database seeding failed: {e}") from e


def seed_db(db_name: str = "WoW.db") -> None:
    """
    Seed the database with random data.
    
    Args:
        db_name: Name of the database to seed
    """
    seeder = DatabaseSeeder()
    seeder.seed_database(db_name)
