from typing import Annotated
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text, String
from config import settings

sync_engine = create_engine(
    url=settings.database_url_psycopg,
    echo=False,
)


session_factory = sessionmaker(sync_engine)


str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f'{col}={getattr(self, col)}')
        return f'<{self.__class__.__name__} {",".join(cols)}>'