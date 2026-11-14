from app.repositories.snakes import create_snake_in_db, get_all_snakes_from_db
from datetime import date

def test_create_snake_in_db(db_session):
    result = create_snake_in_db(session=db_session, name="Larin", age=30)
    assert isinstance(result.id, int)
    assert result.name == "Larin"
    assert result.age == 30
    assert result.added == date.today()


def test_get_all_snakes_from_db(db_session, two_snakes_in_db):
    result = get_all_snakes_from_db(db_session)
    assert len(result) == len(two_snakes_in_db)
    assert result[0].id == two_snakes_in_db[0].id
    assert result[0].name == two_snakes_in_db[0].name
    assert result[0].age == two_snakes_in_db[0].age
    assert result[0].added == two_snakes_in_db[0].added
    assert result[1].id == two_snakes_in_db[1].id
    assert result[1].name == two_snakes_in_db[1].name
    assert result[1].age == two_snakes_in_db[1].age
    assert result[1].added == two_snakes_in_db[1].added