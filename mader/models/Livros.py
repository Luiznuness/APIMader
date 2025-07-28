from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from mader.models.base_model import BaseModel


class Livros(BaseModel):
    __tablename__ = 'livros'

    ano: Mapped[int]
    titulo: Mapped[str] = mapped_column(unique=True)
    id_autor: Mapped[int] = mapped_column(ForeignKey('autores.id'))
