# fastapienv\Scripts\activate.bat
# cd Project3.1-Auth
# uvicorn main:app --reload
# run this to create the databae
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status


from models import Todos
from database import SessionLocal


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # close the database connection after using


db_dependency = Annotated[Session, Depends(get_db)]


# pydantic
# this class will be used for adding new todos (POST request)
# or updating existing todos (PUT request)
class TodoRequest(BaseModel):
    # don't need id
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool


################################################################
# GET
@router.get("/", status_code=status.HTTP_200_OK)
# dependency injection
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)  # path parameter
# status_code=status.HTTP_200_OK is optional, but to be explicit
async def read_todo(
    db: db_dependency, todo_id: int = Path(gt=0)
):  # validation. id must be greater than 0

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    # .first(): to save time. We know there is only one row with this id
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


################################################################
# POST
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)  # getting ready
    db.commit()  # actually adding to the database


################################################################
# PUT
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)
):
    # (db: db_dependency, todo_id: int = Path(gt=0), todo_request: TodoRequest)
    # causes an error because todo_request has to come befor the path parameter

    # get the todo with the id
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.completed = todo_request.completed

    db.add(todo_model)
    db.commit()


################################################################
# DELETE
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):

    # get the todo with the id
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
