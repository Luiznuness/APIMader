from http import HTTPStatus

from fastapi import FastAPI

from mader.database import lifespan
from mader.routers import auth, autores, livros, users
from mader.schemas import Message

app = FastAPI(lifespan=lifespan)

app.include_router(users.routers)
app.include_router(auth.routers)
app.include_router(autores.routers)
app.include_router(livros.routers)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
