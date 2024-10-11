# Test GET /animals
def test_get_animals(client, mock_supabase):
    # Mock response dari Supabase
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
        {'id': 1, 'species': 'dog'},
        {'id': 2, 'species': 'cat'}
    ]

    response = client.get('/animals')
    assert response.status_code == 200

    expected_animals = [
        {'id': 1, 'species': 'dog'},
        {'id': 2, 'species': 'cat'}
    ]

    # Verifikasi bahwa respons sesuai
    for expected in expected_animals:
        assert any(animal['id'] == expected['id'] and animal['species'] == expected['species'] for animal in response.json)


# Test GET /animals/<int:id>
def test_get_animal_by_id_found(client, mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {'id': 1, 'species': 'dog', 'age': 5, 'gender': 'male', 'special_requirements': ''}
    ]

    response = client.get('/animals/1')
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['species'] == 'dog'


# Test GET /animals/<int:id> ketika ID tidak ditemukan
def test_get_animal_by_id_not_found(client, mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

    response = client.get('/animals/999')
    assert response.status_code == 404
    assert response.json['error'] == "404 Not Found: Animal not found"


# Test POST /animals
def test_add_animal(client, mock_supabase):
    # Mock input
    new_animal = {
        'id': 1,
        'species': 'dog',
        'age': 3,
        'gender': 'female',
        'special_requirements': ''
    }

    # Mock response Supabase setelah insert
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [new_animal]

    # Simulate POST request dengan data JSON
    response = client.post('/animals', json={
        'species': 'dog',
        'age': 3,
        'gender': 'female'
    })

    assert response.status_code == 201
    assert response.json['id'] == 1
    assert response.json['species'] == 'dog'
    
#error   
def test_add_animal_require_species(client, mock_supabase):
    # Mock input
    new_animal = {
        'id': 1,
        'age': 3,
        'gender': 'female',
        'special_requirements': ''
    }

    # Mock response Supabase setelah insert
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [new_animal]

    # Simulate POST request dengan data JSON
    response = client.post('/animals', json={
        'age': 3,
        'gender': 'female'
    })

    assert response.status_code == 400
    assert b"Invalid request. 'species' is required" in response.data


# Test PUT /animals/<int:id>
def test_update_animal(client, mock_supabase):
    # Mock data existing animal dan response Supabase setelah update
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {'id': 1, 'species': 'dog', 'age': 5, 'gender': 'male', 'special_requirements': ''}
    ]

    updated_animal = {
        'id': 1,
        'species': 'dog',
        'age': 6,
        'gender': 'male',
        'special_requirements': ''
    }

    mock_supabase.table.return_value.update.return_value.execute.return_value.data = [updated_animal]

    # Simulate PUT request untuk update animal
    response = client.put('/animals/1', json={
        'age': 6
    })

    assert response.status_code == 200
    assert response.json['age'] == 6
    assert response.json['species'] == 'dog'

#error put
def test_update_animal_error_not_found(client, mock_supabase):
    # Mock data existing animal dan response Supabase setelah update
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

    updated_animal = {
        'id': 1,
        'species': 'dog',
        'age': 6,
        'gender': 'male',
        'special_requirements': ''
    }

    mock_supabase.table.return_value.update.return_value.execute.return_value.data = [updated_animal]

    # Simulate PUT request untuk update animal
    response = client.put('/animals/96', json={
        'age': 6
    })

    assert response.status_code == 404
    assert b"Animal not found" in response.data

# Test DELETE /animals/<int:id>
def test_delete_animal(client, mock_supabase):
    # Mock data existing animal dan response Supabase setelah delete
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {'id': 1, 'species': 'dog'}
    ]

    mock_supabase.table.return_value.delete.return_value.execute.return_value.data = None

    # Simulate DELETE request
    response = client.delete('/animals/1')

    assert response.status_code == 200
    assert response.json['result'] == 'Animal deleted'


# Test DELETE /animals/<int:id> ketika ID tidak ditemukan
def test_delete_animal_not_found(client, mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

    response = client.delete('/animals/999')
    assert response.status_code == 404
    assert response.json['error'] == "404 Not Found: Animal not found"