from datetime import datetime

from sqlalchemy import func, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BaseModel(Base):  # pragma: no cover
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        unique=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        unique=False, nullable=True, onupdate=func.now()
    )

    def as_dict(self) -> dict:
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }
