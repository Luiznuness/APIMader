from http import HTTPStatus

import factory
import pytest

from mader.models.Autores import Autores


class AutorFactory(factory.Factory):
    class Meta:
        model = Autores

    name = factory.Faker('pystr', max_chars=10)


def test_created_autor(client, token):
    response = client.post(
        '/autores/',
        json={'name': 'napolen hill'},
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'name': 'Napolen Hill',
    }


@pytest.mark.asyncio
async def test_add_autor_limit(session, token, client):
    session.add_all(AutorFactory.create_batch(5))

    await session.commit()

    response = client.get(
        '/autores/?limit=2',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json()['autores'], list)
    assert len(response.json()['autores']) == 2


@pytest.mark.asyncio
async def test_add_autor_offset(session, token, client):
    session.add_all(AutorFactory.create_batch(5))

    await session.commit()

    response = client.get(
        '/autores/?offset=4',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json()['autores'], list)
    assert len(response.json()['autores']) == 1


@pytest.mark.asyncio
async def test_add_autor_name(session, token, client):
    session.add(AutorFactory(name='Napoleon Hill'))

    await session.commit()

    response = client.get(
        '/autores/?name=Napoleon',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json()['autores'], list)
    assert len(response.json()['autores']) == 1


@pytest.mark.asyncio
async def test_get_autor_id(session, token, client):
    session.add(AutorFactory(name='Napolen Hill'))

    session.add_all(AutorFactory.create_batch(5))

    await session.commit()

    response = client.get(
        '/autores/1',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'name': 'Napolen Hill',
    }


def test_put_autor_id(client, token):
    autor = client.post(
        '/autores/',
        json={
            'name': 'Luiz Gustavo',
        },
        headers={'authorization': f'Bearer {token}'},
    )

    response = client.put(
        f'/autores/{autor.json()["id"]}',
        json={
            'name': 'Napoleon Hill',
        },
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'name': 'Napoleon Hill',
    }


def test_delete_autor(client, token):
    client.post(
        '/autores',
        json={'name': 'napoleon hill'},
        headers={'authorization': f'Bearer {token}'},
    )

    response = client.delete(
        '/autores/1',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Autor deleted'}


def test_error_created_autor(client, token, autor):
    response = client.post(
        '/autores',
        json={'name': 'napoleon hill'},
        headers={'authorization': f'Bearer {token}'},
    )


    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Autor already exists'}


def test_error_get_autor(client, token, autor):
    response = client.get(
        f'autores/{autor.id + 1}',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Autor not found'}


def test_error_put_autor(client, token, autor):
    response = client.put(
        f'autores/{autor.id + 1}',
        json={
            'name': 'alice',
        },
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Autor not found'}


def test_error_delete_autor(client, token, autor):
    response = client.delete(
        f'autores/{autor.id + 1}',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Autor not found'}
