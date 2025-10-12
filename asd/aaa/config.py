"""Configuration settings for the WG Test project."""

import os
from pathlib import Path
from typing import List

# Database configuration
DB_NAME = "WoW.db"
TEMP_DB_NAME = "temp_" + DB_NAME

# Component counts
WEAPONS_COUNT = 20
HULLS_COUNT = 5
ENGINES_COUNT = 6
SHIPS_COUNT = 200

# Component types
COMPONENTS_LIST: List[str] = ["weapon", "hull", "engine"]

# Parameter ranges
MIN_PARAM_VALUE = 1
MAX_PARAM_VALUE = 20

# File paths
PROJECT_ROOT = Path(__file__).parent
LOGS_DIR = PROJECT_ROOT / "logs"
DATA_DIR = PROJECT_ROOT / "data"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Database paths
DB_PATH = DATA_DIR / DB_NAME
TEMP_DB_PATH = DATA_DIR / TEMP_DB_NAME

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = LOGS_DIR / f"{DB_NAME.replace('.db', '')}.log"

# Test configuration
TEST_SHIP_COUNT = 4  # Number of ships to test (reduced from 200 for faster testing)
