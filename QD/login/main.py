# ..\..\fastapienv\Scripts\activate.bat
# cd Project3.2-Auth
# uvicorn main:app --reload

from fastapi import FastAPI
import models

from database import engine
from routers import auth, todos, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# include api endpoints from auth.py and todos.py
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
