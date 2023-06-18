from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from models.base_model import Base


class Advertisements(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    owner = Column(Integer, ForeignKey("users.id"))

    required_fields = ("title", "description")
