from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DATABASE_URL = "postgresql+psycopg://postgres:Sky123@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session