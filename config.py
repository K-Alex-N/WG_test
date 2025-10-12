import os
from pathlib import Path

# Database configuration
DB_NAME = "WoW.db"
TEMP_DB_NAME = "temp_" + DB_NAME

# Component counts
WEAPONS_COUNT = 20
HULLS_COUNT = 5
ENGINES_COUNT = 6
SHIPS_COUNT = 200

# Component types
COMPONENTS_LIST = ["weapon", "hull", "engine"]

# Parameter ranges
MIN_PARAM_VALUE = 1
MAX_PARAM_VALUE = 20

# File paths
PROJECT_ROOT = Path(__file__).parent
LOGS_DIR = PROJECT_ROOT / "logs"
DATA_DIR = PROJECT_ROOT / "data"

# Database paths
DB_PATH = DATA_DIR / DB_NAME
TEMP_DB_PATH = DATA_DIR / TEMP_DB_NAME

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = LOGS_DIR / f"{DB_NAME.replace('.db', '')}.log"