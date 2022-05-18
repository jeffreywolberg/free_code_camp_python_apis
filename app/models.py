from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

# Responsible for defining the columns of our 'posts' table
# within postgres
# Considered an ORM model -- Object Relational Mapping


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        f"{User.__tablename__}.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        f"{User.__tablename__}.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey(
        f"{Post.__tablename__}.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    

