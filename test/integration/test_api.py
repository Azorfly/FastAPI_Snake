def test_get_snake_by_id(client, two_snakes_in_db):
    snake_list = two_snakes_in_db
    response = client.get(f"/snake/{snake_list[0].id}")
    assert response.status_code == 200
    data = response.json()
    assert data['snake_id'] == snake_list[0].id
    assert data['snake_name'] == snake_list[0].name
    assert data['snake_age'] == snake_list[0].age
    assert data['added'] == snake_list[0].added.isoformat()


def test_get_snake_by_id_404(client):
    response = client.get(f"/snake/{-5}")
    assert response.status_code == 404
    assert response.json()['detail'] == "Змеи с ID -5 не существует."


def test_get_snake_by_id_422(client):
    response = client.get('/snake/abc')
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'int_parsing'
    assert response.json()['detail'][0]['loc'] == ['path', 'snake_id']


def test_get_all_snakes_empty(client):
    response = client.get('/snake')
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_snakes(client, two_snakes_in_db):
    response = client.get('/snake')
    assert response.status_code == 200
    assert len(response.json()) == len(two_snakes_in_db)

    for got, expected in zip(response.json(), two_snakes_in_db):
        assert got['snake_id'] == expected.id
        assert got['snake_name'] == expected.name
        assert got['snake_age'] == expected.age
        assert got['added'] == expected.added.isoformat()


def test_add_snake_valid(client):
    response = client.post("/snake", json={"snake_name": "Kaa", "snake_age": 5})
    assert response.status_code == 201
    assert response.json()['message'] == 'Змея добавлена!'
    assert response.json()['name'] == 'Kaa'
    assert response.json()['age'] == 5

    check_existence = client.get(f'/snake/{response.json()['id']}')
    assert check_existence.status_code == 200
    assert check_existence.json()['snake_name'] == response.json()['name']


def test_add_snake_missing_name(client):
    response = client.post('/snake', json={'snake_age': 5})
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'missing'
    assert response.json()['detail'][0]['loc'] == ['body', 'snake_name']


def test_add_snake_missing_age(client):
    response = client.post('/snake', json={'snake_name': 'Kaa'})
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'missing'
    assert response.json()['detail'][0]['loc'] == ['body', 'snake_age']


def test_add_snake_missing_all(client):
    response = client.post('/snake')
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'missing'
    assert response.json()['detail'][0]['loc'] == ['body']


def test_add_snake_invalid_name(client):
    response = client.post('/snake', json={'snake_name': 1, 'snake_age': 5})
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_type'
    assert response.json()['detail'][0]['loc'] == ['body', 'snake_name']


def test_add_snake_invalid_age(client):
    response = client.post('/snake', json={'snake_name': 'Kaa', 'snake_age': 'a'})
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'int_parsing'
    assert response.json()['detail'][0]['loc'] == ['body', 'snake_age']


def test_add_snake_invalid_name_and_age(client):
    response = client.post('/snake', json={'snake_name': 123, 'snake_age': 'abc'})
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_type'
    assert response.json()['detail'][0]['loc'] == ['body', 'snake_name']
    assert response.json()['detail'][1]['type'] == 'int_parsing'
    assert response.json()['detail'][1]['loc'] == ['body', 'snake_age']


def test_update_snake(client, two_snakes_in_db):
    response = client.patch(f'/snake/{two_snakes_in_db[0].id}', json={'snake_name': 'Kaa', 'snake_age': 5})
    assert response.status_code == 200
    assert response.json()['message'] == f'Змея с id {two_snakes_in_db[0].id} обновлена!'
    assert response.json()['updated_snake']['snake_id'] == two_snakes_in_db[0].id
    assert response.json()['updated_snake']['snake_name'] == 'Kaa'
    assert response.json()['updated_snake']['snake_age'] == 5
    assert response.json()['updated_snake']['added'] == two_snakes_in_db[0].added.isoformat()

    check_existence = client.get(f'/snake/{two_snakes_in_db[0].id}')
    assert check_existence.status_code == 200
    assert check_existence.json()['snake_name'] == 'Kaa'
    assert check_existence.json()['snake_age'] == 5

    check_second_snake = client.get(f'/snake/{two_snakes_in_db[1].id}')
    assert check_second_snake.status_code == 200
    assert check_second_snake.json()['snake_name'] == two_snakes_in_db[1].name
    assert check_second_snake.json()['snake_age'] == two_snakes_in_db[1].age


def test_update_snake_name_only(client, two_snakes_in_db):
    response = client.patch(f'/snake/{two_snakes_in_db[0].id}', json={'snake_name': 'Kaa'})
    assert response.status_code == 200
    assert response.json()['updated_snake']['snake_name'] == 'Kaa'
    assert response.json()['updated_snake']['snake_age'] == two_snakes_in_db[0].age

    check_existence = client.get(f'/snake/{two_snakes_in_db[0].id}')
    assert check_existence.json()['snake_name'] == 'Kaa'
    assert check_existence.json()['snake_age'] == two_snakes_in_db[0].age


def test_update_snake_age_only(client, two_snakes_in_db):
    response = client.patch(f'/snake/{two_snakes_in_db[0].id}', json={'snake_age': 5})
    assert response.status_code == 200
    assert response.json()['updated_snake']['snake_name'] == two_snakes_in_db[0].name
    assert response.json()['updated_snake']['snake_age'] == 5

    check_existence = client.get(f'/snake/{two_snakes_in_db[0].id}')
    assert check_existence.json()['snake_name'] == two_snakes_in_db[0].name
    assert check_existence.json()['snake_age'] == 5


def test_update_snake_empty_body(client, two_snakes_in_db):
    response = client.patch(f'/snake/{two_snakes_in_db[0].id}', json={})
    assert response.status_code == 200
    assert response.json()['updated_snake']['snake_id'] == two_snakes_in_db[0].id
    assert response.json()['updated_snake']['snake_name'] == two_snakes_in_db[0].name
    assert response.json()['updated_snake']['snake_age'] == two_snakes_in_db[0].age


def test_update_snake_404(client):
    response = client.patch('/snake/-5', json={'snake_name': 'Kaa'})
    assert response.status_code == 404
    assert response.json()['detail'] == 'Змеи с ID -5 не существует.'


def test_update_snake_422_id(client):
    response = client.patch('/snake/abc', json={'snake_name': 'Kaa'})
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'int_parsing'
    assert response.json()['detail'][0]['loc'] == ['path', 'snake_id']


def test_update_snake_missing_body(client, two_snakes_in_db):
    response = client.patch(f'/snake/{two_snakes_in_db[0].id}')
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'missing'
    assert response.json()['detail'][0]['loc'] == ['body']


def test_update_snake_invalid_name(client, two_snakes_in_db):
    response = client.patch(f'/snake/{two_snakes_in_db[0].id}', json={'snake_name': 123})
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_type'
    assert response.json()['detail'][0]['loc'] == ['body', 'snake_name']


def test_update_snake_invalid_age(client, two_snakes_in_db):
    response = client.patch(f'/snake/{two_snakes_in_db[0].id}', json={'snake_age': 'abc'})
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'int_parsing'
    assert response.json()['detail'][0]['loc'] == ['body', 'snake_age']

def test_delete_snake(client, two_snakes_in_db):
    response = client.delete(f'/snake/{two_snakes_in_db[0].id}')
    assert response.status_code == 200
    assert response.json()['message'] == f'Змея с ID {two_snakes_in_db[0].id} удалена.'

    check_existence = client.get(f'/snake/{two_snakes_in_db[0].id}')
    assert check_existence.status_code == 404

    check_second_snake = client.get(f'/snake/{two_snakes_in_db[1].id}')
    assert check_second_snake.status_code == 200
    assert check_second_snake.json()['snake_name'] == two_snakes_in_db[1].name


def test_delete_snake_404(client):
    response = client.delete('/snake/-5')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Змеи с ID -5 не существует.'


def test_delete_snake_422_id(client):
    response = client.delete('/snake/abc')
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'int_parsing'
    assert response.json()['detail'][0]['loc'] == ['path', 'snake_id']