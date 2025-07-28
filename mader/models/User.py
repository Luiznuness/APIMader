from sqlalchemy import inspect
from sqlalchemy.orm import Mapped, mapped_column

from mader.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    def as_dict(self) -> dict:
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }
