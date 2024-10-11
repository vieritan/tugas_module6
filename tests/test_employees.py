def test_get_employees(client, mock_supabase):
    # Mock response dari Supabase
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
        {'id': 1, 'name': 'jon', 'email': 'jon@gmail.com', 'phone_number': '085656565656', 'role': 'staff', 'schedule': 'morning'},
        {'id': 2, 'name': 'nana', 'email': 'nana@gmail.com', 'phone_number': '085656565656', 'role': 'staff', 'schedule': 'morning'}
    ]

    response = client.get('/employees')
    assert response.status_code == 200

    expected_employees = [
        {'id': 1, 'name': 'jon', 'email': 'jon@gmail.com', 'phone_number': '085656565656', 'role': 'staff', 'schedule': 'morning'},
        {'id': 2, 'name': 'nana', 'email': 'nana@gmail.com', 'phone_number': '085656565656', 'role': 'staff', 'schedule': 'morning'}
    ]

    # Verifikasi bahwa respons sesuai
    for expected in expected_employees:
        assert any(employee['id'] == expected['id'] and employee['name'] == expected['name'] for employee in response.json)

def test_get_employees_by_id_found(client, mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {'id': 1, 'name': 'jan', 'email': 'jan@gmail.com', 'phone_number': '085656565656', 'role': 'staff', 'schedule': 'morning'}
    ]

    response = client.get('/employees/1')
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['name'] == 'jan'
    
def test_get_employees_by_id_not_found(client, mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

    response = client.get('/employees/999')
    assert response.status_code == 404
    assert response.json['error'] == "404 Not Found: employee not found"
    
def test_add_employee(client, mock_supabase):
    # Mock input
    new_employee = {
        'id': 1,
        'name': 'ade',
        'email': 'ade@gmail.com',
        'phone_number': '085152252532',
        'role': 'staff',
        'schedule': 'malam'
    }

    # Mock response Supabase setelah insert
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [new_employee]

    # Simulate POST request dengan data JSON
    response = client.post('/employees', json={
        'name': 'ade',
        'email': 'ade@gmail.com',
        'phone_number': '085152252532',
        'role': 'staff',
        'schedule': 'malam'
    })

    assert response.status_code == 201
    assert response.json['id'] == 1
    assert response.json['name'] == 'ade'

#error   
def test_add_employee_require_species(client, mock_supabase):
    # Mock input
    new_employee = {
        'email': 'jon@gmail.com',
        'phone_number': '085656565656',
        'role': 'manager',
        'schedule': 'morning'
    }

    # Mock response Supabase setelah insert
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [new_employee]

    # Simulate POST request dengan data JSON
    response = client.post('/employees', json={
        'email': 'jon@gmail.com',
        'phone_number': '085656565656'
    })

    assert response.status_code == 400
    assert b"Invalid request. 'name' is required" in response.data
    
def test_update_employee(client, mock_supabase):
    # Mock data existing animal dan response Supabase setelah update
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {'id': 1, 'name': 'jon', 'email': 'jon@gmail.com', 'phone_number': '085656565656', 'role': 'staff', 'schedule': 'morning'}
    ]

    updated_employee = { # data output
        'id': 1,
        'name': 'jon',
        'email': 'jon@gmail.com',
        'phone_number': '085656565656',
        'role': 'manager',
        'schedule': 'morning'
    }

    mock_supabase.table.return_value.update.return_value.execute.return_value.data = [updated_employee]

    # Simulate PUT request untuk update animal
    response = client.put('/employees/1', json={
        'role': 'manager'
    })

    assert response.status_code == 200
    assert response.json['role'] == 'manager'
    assert response.json['name'] == 'jon'
 
#error put   
def test_update_employee_error_not_found(client, mock_supabase):
    # Mock data existing animal dan response Supabase setelah update
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

    updated_employee = { # data output
        'id': 1,
        'name': 'jon',
        'email': 'jon@gmail.com',
        'phone_number': '085656565656',
        'role': 'manager',
        'schedule': 'morning'
    }

    mock_supabase.table.return_value.update.return_value.execute.return_value.data = [updated_employee]

    # Simulate PUT request untuk update animal
    response = client.put('/employees/69', json={
        'role': 'manager'
    })

    assert response.status_code == 404
    assert b"employee not found" in response.data
    
    
# Test DELETE /animals/<int:id>
def test_delete_employee(client, mock_supabase):
    # Mock data existing animal dan response Supabase setelah delete
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {'id': 1, 'name': 'jon'}
    ]

    mock_supabase.table.return_value.delete.return_value.execute.return_value.data = None

    # Simulate DELETE request
    response = client.delete('/employees/1')

    assert response.status_code == 200
    assert response.json['result'] == 'employee deleted'
    
# Test DELETE /animals/<int:id> ketika ID tidak ditemukan
def test_delete_employee_not_found(client, mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

    response = client.delete('/employees/999')
    assert response.status_code == 404
    assert b"employee not found" in response.data