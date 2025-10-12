# WG Test Project

A comprehensive database testing and management system for ship components and configurations.

## Overview

This project implements a robust database testing framework that:
- Creates and manages SQLite databases with ship, weapon, hull, and engine data
- Implements randomization algorithms for testing data integrity
- Provides comprehensive test coverage with pytest
- Includes a CLI interface for database operations
- Features proper logging, error handling, and type safety

## Features

### 🗄️ Database Management
- **Schema Validation**: Automatic database schema verification
- **Data Integrity**: Foreign key constraints and parameter validation
- **Performance**: Optimized with indexes for better query performance
- **Backup/Restore**: Temporary database creation for testing

### 🧪 Testing Framework
- **Comprehensive Tests**: 12+ test cases covering all scenarios
- **Parametrized Testing**: Efficient test execution with pytest.mark.parametrize
- **Data Validation**: Automatic verification of randomized data
- **Error Reporting**: Detailed failure messages with context

### 🛠️ Developer Experience
- **CLI Interface**: Easy-to-use command-line tools
- **Logging**: Comprehensive logging with configurable levels
- **Type Safety**: Full type hints throughout the codebase
- **Error Handling**: Robust error handling with custom exceptions
- **Documentation**: Comprehensive docstrings and comments

## Project Structure

```
WG_test/
├── cli.py                 # Command-line interface
├── config.py             # Configuration settings
├── requirements.txt      # Dependencies
├── README.md            # This file
├── db/                  # Database layer
│   ├── __init__.py
│   ├── conn_db.py       # Database connections
│   ├── create_db.py     # Database creation
│   ├── logger.py        # Logging configuration
│   ├── models.py        # Data models
│   ├── seed_db.py       # Data seeding
│   ├── tmp_db.py        # Temporary database management
│   └── utils.py         # Utility functions
└── tests/               # Test suite
    ├── __init__.py
    ├── conftest.py      # Test configuration
    └── test_ships.py    # Main test cases
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd WG_test
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python cli.py status
   ```

## Usage

### Command Line Interface

The project includes a comprehensive CLI for all operations:

```bash
# Create the main database
python cli.py create-db

# Seed the database with data
python cli.py seed-db

# Create temporary database for testing
python cli.py create-temp-db

# Run tests
python cli.py run-tests

# Run tests with verbose output and coverage
python cli.py run-tests -v --coverage

# Show project status
python cli.py status

# Clean up temporary files
python cli.py cleanup
```

### Running Tests

#### Basic Test Execution
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_ships.py

# Run with coverage report
pytest --cov=db --cov-report=html
```

#### Test Configuration
- **Test Count**: 12 tests (4 ships × 3 components)
- **Test Scope**: Session-scoped fixtures for database setup
- **Randomization**: Automatic data randomization for testing
- **Validation**: Comprehensive data integrity checks

### Programmatic Usage

```python
from db.create_db import create_db, verify_db_schema
from db.seed_db import seed_db
from db.tmp_db import create_tmp_db, drop_tmp_db

# Create and seed database
create_db("my_database.db")
seed_db("my_database.db")

# Verify schema
if verify_db_schema("my_database.db"):
    print("Database schema is valid")

# Create temporary database for testing
create_tmp_db()
# ... perform tests ...
drop_tmp_db()
```

## Configuration

The project uses `config.py` for all configuration settings:

```python
# Database settings
DB_NAME = "WoW.db"
TEMP_DB_NAME = "temp_WoW.db"

# Component counts
WEAPONS_COUNT = 20
HULLS_COUNT = 5
ENGINES_COUNT = 6
SHIPS_COUNT = 200

# Parameter ranges
MIN_PARAM_VALUE = 1
MAX_PARAM_VALUE = 20

# Test configuration
TEST_SHIP_COUNT = 4  # Reduced for faster testing
```

## Database Schema

### Ships Table
```sql
CREATE TABLE ships (
    ship TEXT PRIMARY KEY,
    weapon TEXT NOT NULL,
    hull TEXT NOT NULL,
    engine TEXT NOT NULL,
    FOREIGN KEY (weapon) REFERENCES weapons(weapon),
    FOREIGN KEY (hull) REFERENCES hulls(hull),
    FOREIGN KEY (engine) REFERENCES engines(engine)
);
```

### Weapons Table
```sql
CREATE TABLE weapons (
    weapon TEXT PRIMARY KEY,
    reload_speed INTEGER NOT NULL CHECK (reload_speed >= 1 AND reload_speed <= 20),
    rotational_speed INTEGER NOT NULL CHECK (rotational_speed >= 1 AND rotational_speed <= 20),
    diameter INTEGER NOT NULL CHECK (diameter >= 1 AND diameter <= 20),
    power_volley INTEGER NOT NULL CHECK (power_volley >= 1 AND power_volley <= 20),
    count INTEGER NOT NULL CHECK (count >= 1 AND count <= 20)
);
```

### Hulls Table
```sql
CREATE TABLE hulls (
    hull TEXT PRIMARY KEY,
    armor INTEGER NOT NULL CHECK (armor >= 1 AND armor <= 20),
    type INTEGER NOT NULL CHECK (type >= 1 AND type <= 20),
    capacity INTEGER NOT NULL CHECK (capacity >= 1 AND capacity <= 20)
);
```

### Engines Table
```sql
CREATE TABLE engines (
    engine TEXT PRIMARY KEY,
    power INTEGER NOT NULL CHECK (power >= 1 AND power <= 20),
    type INTEGER NOT NULL CHECK (type >= 1 AND type <= 20)
);
```

## Testing Strategy

### Test Types

1. **Component Tests**: Verify ship components (weapon, hull, engine) have changed
2. **Parameter Tests**: Verify component parameters have been randomized
3. **Schema Tests**: Verify database schema integrity
4. **Data Tests**: Verify data presence and consistency

### Test Execution Flow

1. **Setup**: Create main database and seed with data
2. **Randomization**: Create temporary database with randomized data
3. **Comparison**: Compare original and randomized data
4. **Validation**: Verify changes were applied correctly
5. **Cleanup**: Remove temporary files

## Logging

The project includes comprehensive logging:

```python
from db.logger import logger

# Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
logger.info("Operation completed successfully")
logger.error("Operation failed: {error}")
logger.debug("Detailed debug information")
```

Log files are stored in the `logs/` directory.

## Error Handling

The project implements robust error handling:

- **Custom Exceptions**: `DatabaseError` for database-related issues
- **Context Managers**: Automatic resource cleanup
- **Validation**: Input validation and parameter checking
- **Logging**: Comprehensive error logging and reporting

## Development

### Code Quality

The project follows Python best practices:

- **Type Hints**: Full type annotation throughout
- **Docstrings**: Comprehensive documentation
- **PEP 8**: Code style compliance
- **Error Handling**: Robust exception handling
- **Logging**: Structured logging throughout

### Testing

- **Coverage**: Aim for 100% test coverage
- **Parametrization**: Efficient test execution
- **Fixtures**: Reusable test components
- **Validation**: Comprehensive data validation

## Performance

### Optimizations

- **Database Indexes**: Optimized query performance
- **Batch Operations**: Efficient data insertion
- **Connection Pooling**: Optimized database connections
- **Memory Management**: Efficient resource usage

### Monitoring

- **Logging**: Performance monitoring through logs
- **Metrics**: Database operation timing
- **Profiling**: Code performance analysis

## Troubleshooting

### Common Issues

1. **Database Locked**: Ensure all connections are properly closed
2. **Schema Mismatch**: Run schema verification
3. **Test Failures**: Check log files for detailed error information
4. **Permission Errors**: Ensure proper file permissions

### Debug Mode

Enable debug logging for detailed information:

```bash
export LOG_LEVEL=DEBUG
python cli.py run-tests
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the logs in the `logs/` directory
2. Review the test output for error details
3. Check the project documentation
4. Create an issue in the repository
