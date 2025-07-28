from http import HTTPStatus


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
