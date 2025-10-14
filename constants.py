# Test failure
COMPARE_COMPONENTS_FAIL_MESSAGE = (
    "{ship_id}, {comp}\n\tExpected {orig_comp}, was {changed_comp}"
)

COMPARE_PARAMS_FAIL_MESSAGE = (
    "{ship_id}, {comp_id}\n\t{param}: expected {orig_value}, was {changed_value}"
)

# Error messages
UNKNOWN_COMPONENT_MESSAGE = "Unknown component: '{comp}'"
SHIP_NOT_FOUND_MESSAGE = "Ship not found: {ship_id}"
COMPONENT_NOT_FOUND_MESSAGE = "Component not found: {comp_id}"

# BD logging messages
CONNECTING_TO_DB = "Connecting to database: {db_name}"
DB_ERROR = "Database error in {db_name}, transaction rolled back: {e}"
UNEXPECTED_ERROR = "Unexpected error in {db_name}: {e}"
CLOSED_CONNECTION = "Closed connection to {db_name}"
CURSOR_ERROR = "Cursor error in {db_name}: {e}"

TABLE_CREATED = "Table {table} created successfully"

DB_SEEDING_START = "Starting database seeding"
DB_POPULATED_SUCCESSFULLY = "Database populated successfully"

TMP_DB_CREATED = "Created temporary database: {db_name}"
TMP_DB_REMOVED = "Removed temporary database: {db_name}"

# Repository logging
REPO_SHIP_FIND_START = "Finding ship by ID: {ship_id} in database: {db_name}"
REPO_SHIP_FIND_SUCCESS = "Ship found: {ship_id}"
REPO_SHIP_FIND_NOT_FOUND = "Ship not found: {ship_id} in database: {db_name}"
REPO_SHIP_FIND_ALL = "Retrieving all ships from database: {db_name}"
REPO_SHIP_FIND_ALL_SUCCESS = "Retrieved {count} ships from database: {db_name}"
REPO_SHIP_UPDATE = "Updating ship {ship_id}: setting {component} to {component_id} in {db_name}"
REPO_SHIP_UPDATE_SUCCESS = "Successfully updated ship {ship_id}"
REPO_COMPONENT_FIND_START = "Finding component {component_type}: {component_id} in database: {db_name}"
REPO_COMPONENT_FIND_SUCCESS = "Component found: {component_id}"
REPO_COMPONENT_FIND_NOT_FOUND = "Component not found: {component_id} in database: {db_name}"
REPO_COMPONENT_FIND_ALL = "Retrieving all components from table: {component_table} in database: {db_name}"
REPO_COMPONENT_FIND_ALL_SUCCESS = "Retrieved {count} components from {component_table}"
REPO_COMPONENT_UPDATE = "Updating component {component_id}: setting {param_name} to {param_value}"
REPO_COMPONENT_UPDATE_SUCCESS = "Successfully updated component {component_id}"

# Service logging
SERVICE_GET_SHIP_START = "Service: Getting ship {ship_id} from {db_name}"
SERVICE_GET_SHIP_SUCCESS = "Service: Successfully retrieved ship {ship_id}"
SERVICE_GET_SHIP_ERROR = "Service: Failed to get ship {ship_id}: {error}"
SERVICE_GET_COMPONENT_START = "Service: Getting {component_type} component {component_id} from {db_name}"
SERVICE_GET_COMPONENT_SUCCESS = "Service: Successfully retrieved component {component_id}"
SERVICE_GET_COMPONENT_ERROR = "Service: Failed to get component {component_id}: {error}"
SERVICE_COMPARE_SHIPS_START = "Service: Comparing {component_type} between ships"
SERVICE_COMPARE_SHIPS_MATCH = "Service: Ships have matching {component_type}: {component_id}"
SERVICE_COMPARE_SHIPS_DIFFER = "Service: Ships have different {component_type}: {orig} vs {changed}"
SERVICE_COMPARE_PARAMS_START = "Service: Comparing parameters for component {component_id}"
SERVICE_COMPARE_PARAMS_MATCH = "Service: All parameters match for component {component_id}"
SERVICE_COMPARE_PARAMS_DIFFER = "Service: Parameter '{param}' differs: {orig_value} vs {changed_value}"
SERVICE_UPDATE_SHIP = "Service: Updating ship {ship_id} component {component_type} to {component_id}"
SERVICE_UPDATE_COMPONENT = "Service: Updating component {component_id} parameter {param_name}"

# Test setup logging
TEST_RANDOMIZE_SHIP_START = "Randomizing ship: {ship_id}"
TEST_RANDOMIZE_SHIP_COMPLETE = "Ship {ship_id} randomized: {component} set to {component_id}"
TEST_RANDOMIZE_COMPONENT_START = "Randomizing component: {component_id}"
TEST_RANDOMIZE_COMPONENT_COMPLETE = "Component {component_id} randomized: {param} set to {value}"
TEST_RANDOMIZE_ALL_SHIPS = "Randomizing ships"
TEST_RANDOMIZE_ALL_COMPONENTS = "Randomizing {count} {component_type} components"
TEST_RANDOMIZE_TMP_DB_START = "Randomizing temporary database"
TEST_RANDOMIZE_TMP_DB_COMPLETED = "Temporary database randomization completed"

COMPARE_COMPONENTS_IN_SHIP = "Compare components in ship: {ship_id}"
COMPARE_PARAMS_IN_COMPONENT = "Compare parameters in component: {component_type}"