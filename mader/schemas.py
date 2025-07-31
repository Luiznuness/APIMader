from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Message(BaseModel):
    message: str


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)


class CreatedUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class ListUser(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class Books(BaseModel):
    ano: int
    titulo: str = Field(default=None, min_length=2, max_length=30)


class FilterBooks(FilterPage):
    ano: int | None = Field(default=None, le=datetime.now().year)
    titulo: str | None = Field(default=None, min_length=2, max_length=30)


class BooksPublic(Books):
    id: int
    id_autor: int


class BookAutor(BooksPublic):
    autor: str

    model_config = ConfigDict(from_attributes=True)


class UpdateBook(BaseModel):
    ano: int | None
    titulo: str | None = Field(default=None, min_length=2, max_length=30)
    id_book: int


class ListBooks(BaseModel):
    books: list[BookAutor]


class Autor(BaseModel):
    name: str


class AutorPublic(Autor):
    id: int


class ListAutorPublic(BaseModel):
    autores: list[AutorPublic]


class FilterAutor(FilterPage):
    name: str | None = Field(default=None, min_length=2, max_length=22)
