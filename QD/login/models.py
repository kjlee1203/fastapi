from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class Todos(Base):
    __tablename__ = "todos"

    # make table columns
    id = Column(
        Integer, primary_key=True, index=True
    )  # id is unique (primary_key) for each row
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(
        Integer, ForeignKey("users.id")
    )  # owner_id is a foreign key to the users table
