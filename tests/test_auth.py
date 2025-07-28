from datetime import datetime, timedelta
from http import HTTPStatus

from freezegun import freeze_time


def test_error_token_incorrect(client, user):
    response = client.put(
        f'users/{user.id}',
        json={
            'username': 'alice',
            'email': 'alice@exemple.com',
            'password': 'alice',
        },
        headers={'authorization': 'Bearer test'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_error_created_token_user_not_found(client):
    response = client.post(
        '/auth/token', data={'username': 'luiz@test.com', 'password': 'test'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email ou password'}


def test_error_created_token_password_invalid(client, user):
    response = client.post(
        '/auth/token', data={'username': user.email, 'password': 'luiz'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email ou password'}


def test_error_token_expired(client, user):
    with freeze_time(datetime.now()):
        response = client.post(
            'auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.CREATED
        assert 'access_token' in response.json()
        token = response.json()['access_token']

    with freeze_time(datetime.now() + timedelta(minutes=30)):
        response = client.put(
            f'users/{user.id}',
            json={
                'username': 'alice',
                'email': 'alice@exemple.com',
                'password': 'alice',
            },
            headers={'authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token(client, token):
    response = client.post(
        'auth/refresh-token',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()
    assert response.json()['token_type'] == 'Bearer'


def test_error_token_expired_refresh_token(client, user):
    with freeze_time(datetime.now()):
        response = client.post(
            'auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.CREATED
        assert 'access_token' in response.json()
        token = response.json()['access_token']

    with freeze_time(datetime.now() + timedelta(minutes=30)):
        response = client.post(
            'auth/refresh-token',
            headers={'authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
