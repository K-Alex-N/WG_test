import pytest

from db.seed_db import seed_db
from db.create_db import create_db


@pytest.fixture(scope='session')
def db():
    create_db()
    seed_db()
    yield
    # drop_db