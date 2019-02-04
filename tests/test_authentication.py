import pytest


@pytest.mark.usefixtures('request_ctx')
def test_bad_authentication(xhr_client):
    response = xhr_client.post(
        '/auth', data={'username': 'wrong', 'password': 'wrong'}
    )
    assert response.status_code == 401
    assert response.json == {
        'description': 'Invalid credentials',
        'error': 'Bad Request',
        'status_code': 401,
    }


@pytest.mark.usefixtures('request_ctx')
def test_successful_authentication(xhr_client):
    response = xhr_client.post(
        '/auth', data={'username': 'fakeuser', 'password': 'fakepassword'}
    )
    assert response.status_code == 200
    assert response.json.get('access_token') is not None
    assert type(response.json.get('access_token')) == str
    assert len(response.json.get('access_token'))
