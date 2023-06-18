import uuid

from sqlalchemy import Column, Integer, Uuid, ForeignKey

from models.base_model import Base


class Tokens(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(Uuid, unique=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey('users.id'))
