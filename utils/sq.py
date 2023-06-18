import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models.base_model import Base


class Sq:
    DB = os.getenv("DATABASE", "sqlite:///database/database.db")
    ENGINE = None

    @classmethod
    def create_engine(cls):
        cls.ENGINE = create_engine(cls.DB)
        return cls

    @classmethod
    def get_session(cls) -> Session:
        session = sessionmaker(bind=cls.ENGINE)
        return session()

    @classmethod
    def create_tables(cls):
        Base.metadata.create_all(cls.ENGINE)
