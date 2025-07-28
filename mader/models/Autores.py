from sqlalchemy.orm import Mapped, mapped_column, relationship

from mader.models.base_model import BaseModel
from mader.models.Livros import Livros


class Autores(BaseModel):
    __tablename__ = 'autores'

    name: Mapped[str] = mapped_column(unique=True)
    livros: Mapped[list[Livros]] = relationship(
        cascade='all, delete-orphan',
        lazy='selectin',
    )
