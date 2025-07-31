from http import HTTPStatus

import factory
import pytest

from mader.models.Livros import Livros


class LivrosFactory(factory.Factory):
    class Meta:
        model = Livros

    titulo = factory.Sequence(lambda n: f'Pense{n}')
    ano = factory.Faker('random_int', min=1990, max=2025)
    id_autor: int


def test_created_livro(client, token, autor):
    response = client.post(
        f'/livros/{autor.id}',
        json={
            'ano': 1937,
            'titulo': 'pense enriqueça',
        },
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'ano': 1937,
        'titulo': 'Pense Enriqueça',
        'id_autor': 1,
    }


@pytest.mark.asyncio
async def test_get_books_filter_titulo(livro, autor, token, client):
    response = client.get(
        '/livros/?titulo=Pense',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': [{
        'ano': 1937,
        'titulo': 'Pense Enriqueça',
        'id': 1,
        'id_autor': autor.id,
        'autor': 'Napoleon Hill',
    }]}


def test_get_books_filter_ano(livro, autor, token, client):
    response = client.get(
        '/livros/?ano=1937',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': [{
        'ano': 1937,
        'titulo': 'Pense Enriqueça',
        'id': 1,
        'id_autor': autor.id,
        'autor': 'Napoleon Hill',
    }]}

def test_created_livro_error_autor(client, token, autor):
    response = client.post(
        f'/livros/{autor.id + 1}',
        json={
            'ano': 1937,
            'titulo': 'pense enriqueça',
        },
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Autor not exists'}


def test_patch_livro(client, autor, livro, token):
    response = client.patch(
        f'/livros/{autor.id}',
        json={
            'ano': 2011,
            'titulo': 'mais esperto que o diabo',
            'id_book': livro.id,
        },
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'ano': 2011,
        'titulo': 'mais esperto que o diabo'.strip().title(),
        'id': 1,
        'id_autor': autor.id,
    }


def test_patch_livro_error_autor(client, autor, livro, token):
    response = client.patch(
        f'/livros/{autor.id + 1}',
        json={
            'ano': 2011,
            'titulo': 'mais esperto que o diabo',
            'id_book': livro.id,
        },
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Autor not exists'}