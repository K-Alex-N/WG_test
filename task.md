# Home Task Goal

The Home Task is designed to assess:
- Work with Python
- Level of programming culture and knowledge

The task will show the candidate what they will have to do in our team.  
Despite this, the data in the task has a very simplified schema compared to the real one.

## Requirements for the Completed Task

- **Python version**: 3.10 or higher
- **Testing framework**: `pytest`
- **Parameterization**: Use `pytest.mark.parametrize` or the `pytest_generate_tests` hook
- **Test count**: Should be **600 tests** in total after run
- **Deliverables**:
  - Script that creates and populates the source database
  - Python module with tests
  - `conftest.py` with fixtures/hooks (optional)
- **Code style**: PEP8


## Database Creation Script

Write a Python script that creates a SQLite database according to the specified schema.

- **Primary keys**:  
  The following entities must use **string fields** as primary keys:
  - `weapon
- ## II Task — Random Data Population

Create a script that will randomly fill in the values in the created database.

- **Naming convention**:  
  Use simple, sequential names that fit perfectly:
  - `Ship-1`, `Ship-2`, ...
  - `Weapon-1`, `Weapon-2`, ...
  - and so on


## III Task — Session-Scoped Fixture for Randomization

Create a **session-scope fixture** that performs the following:

- Retrieves the **current state** of the database
- Creates a **temporary new database** with randomized values

### Randomization Logic

A. For each ship:
- Randomly change **one** of its components: `hull`, `gun`, or `engine`

B. For each changed component:
- Randomly select **one parameter**
- Assign it a **random value** from the allowable range (see above)

## IV Task — Autotests for Database Comparison

Create **autotests** that compare data from the original database with the randomized one.

### A. Per-Ship Test Coverage

- Each ship should have **3 tests**:
  - One for its **gun**
  - One for its **hull**
  - One for its **engine**

### B. Test Failure Conditions

A test should **fail** in the following cases:

1. If the value of a **component parameter** does not match what it was before the randomizer was run  
   **Output example**:


2. If the **gun, hull, or engine** of the ship has changed  
**Output example**:
