from pathlib import Path

# Database configuration
DB_NAME = "WoW.db"
TEMP_DB_NAME = "temp_" + DB_NAME

# Component counts
WEAPONS_COUNT = 20
HULLS_COUNT = 5
ENGINES_COUNT = 6
SHIPS_COUNT = 200

# Parameter value ranges
MIN_PARAM_VALUE = 1
MAX_PARAM_VALUE = 20

# Component types
COMPONENTS = ["weapon", "hull", "engine"]

# paths
PROJECT_ROOT = Path(__file__).parent
LOGS_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOGS_DIR / "WoW.log"
