import pytest
from testcontainers.community.postgres import PostgresContainer
from sqlalchemy import create_engine
from app.models.snake import Base
from sqlalchemy.orm import Session
from app.models.snake import Snakes
from fastapi.testclient import TestClient
from main import app
from app.db_session import get_session


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:16", driver="psycopg") as pg:
        DATABASE_URL = pg.get_connection_url()
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        yield engine


@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    with Session(bind=connection, join_transaction_mode="create_savepoint") as session:
        yield session

    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def two_snakes_in_db(db_session):
    snake1 = Snakes(name="Larin", age=30)
    snake2 = Snakes(name="Lucky", age=32)
    db_session.add_all([snake1, snake2])
    db_session.flush()
    return [snake1, snake2]


@pytest.fixture(scope="function")
def client(db_session):
    def session_test():
        yield db_session

    app.dependency_overrides[get_session] = session_test
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()