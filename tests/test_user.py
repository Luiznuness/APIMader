from http import HTTPStatus

from mader.schemas import UserPublic


def test_created_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'test',
        'email': 'test@test.com',
    }


def test_username_exists(client, user):
    response = client.post(
        '/users',
        json={
            'username': user.username,
            'email': 'luiz@test.com',
            'password': 'test',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_email_exists(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'luiz',
            'email': user.email,
            'password': 'test',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_get_users(client, user, other_user):
    response = client.get(
        'users/',
    )

    user_json = UserPublic.model_validate(user).model_dump()

    other_user_json = UserPublic.model_validate(other_user).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_json, other_user_json]}


def test_get_users_limit(client, user, other_user):
    response = client.get(
        'users/?limit=1',
    )

    user_json = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_json]}


def test_get_users_offset(client, user, other_user):
    response = client.get(
        'users/?offset=1',
    )

    other_user_json = {
        'id': other_user.id,
        'username': other_user.username,
        'email': other_user.email,
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [other_user_json]}


def test_get_user(client, user):
    response = client.get(
        f'users/{user.id}',
    )

    user_json = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_json


def test_error_get_user(client, user):
    response = client.get(
        f'users/{user.id + 1}',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_put_user(client, token):
    response = client.put(
        'users/1',
        json={
            'username': 'alice',
            'email': 'alice@test.com',
            'password': 'alice',
        },
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@test.com',
    }


def test_error_put_user_permissions(client, token, other_user):
    response = client.put(
        f'users/{other_user.id}',
        json={
            'username': 'alice',
            'email': 'alice@test.com',
            'password': 'alice',
        },
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_error_put_user_integrity(client, token, other_user):
    response = client.put(
        'users/1',
        json={
            'username': 'alice',
            'email': other_user.email,
            'password': 'alice',
        },
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_delete_user(client, token):
    response = client.delete(
        'users/1',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_error_delete_user(client, token, other_user):
    response = client.delete(
        f'users/{other_user.id}',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
