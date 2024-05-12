from database import Base
from sqlalchemy import Column, Integer, String, Boolean


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
