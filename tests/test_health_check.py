

def test_health_check(client):
    response = client.get('/health-check')

    assert b'Ok' in response.data
    assert response.status_code == 200
