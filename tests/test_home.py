def test_get_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"hello world" in response.data