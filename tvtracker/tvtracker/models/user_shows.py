from sqlalchemy import (
    Column,
    Integer,
    Text,
    Table,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from .meta import Base


class UserShows(Base):
    __tablename__ = "user_shows"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    showId = Column(Integer)
    userId = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User')