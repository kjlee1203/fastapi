from fastapi import FastAPI

app = FastAPI()


@app.get("/api-endpoint")
# make this as api endpoint
# url 127.0.0.1:8000/api-endpoint
async def first_api():
    # asynchronous function. can pause and resume execution
    # async is optional for FastAPI
    return {"message": "Hello, World!"}


# fastapienv\Scripts\activate.bat
# uvicorn Project1.books1:app --reload
# deactivate
