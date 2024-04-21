from typing import Optional
from fastapi import FastAPI, Path  # for validating path parameters
from pydantic import BaseModel, Field  # for validation

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):  # BaseModel, Field are from pydantic
    id: Optional[int] = None  # now we don't need to pass id in the request
    # id: Optional[int] = Field(title="ID is not needed") # not working
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)  # rating should be between 1 and 5
    published_date: int = Field(gt=1999, lt=2031)

    # display example in the swagger, without id
    class Config:
        json_schema_extra = {
            "example": {
                "title": "A New Book",
                "author": "codingwithroby",
                "description": "A new description",
                "rating": 5,
                "published_date": 2029,
            }
        }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5, 2030),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5, 2030),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5, 2029),
    Book(4, "HP1", "Author 1", "Book Description", 2, 2028),
    Book(5, "HP2", "Author 2", "Book Description", 3, 2027),
    Book(6, "HP3", "Author 3", "Book Description", 1, 2026),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


# fetch a book by id
# http://127.0.0.1:8000/books/5
@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):  # books_id is greater than 0
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {"error": "Book not found"}


# filter books by rating
# this won't interfere with the above endpoint
# because we use query parameter
# http://127.0.0.1:8000/books/?book_rating=3
@app.get("/books/")
async def read_books_by_rating(book_rating: int):
    return [book for book in BOOKS if book.rating == book_rating]


@app.get("/books/publish/")
async def read_books_by_publish_date(publish_date: int):
    return [book for book in BOOKS if book.published_date == publish_date]


@app.post("/create-book")
async def create_book(
    book_request: BookRequest,
):  # book_request now has type BookRequest
    new_book = Book(**book_request.model_dump())  # convert the request to Book object
    BOOKS.append(find_book_id(new_book))


# what about the id?
# we want to assign id in the chronological order
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    return book


@app.put("/books/{update_books}")
async def update_books(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            return {"message": "Book updated successfully"}


@app.delete("/books/{book_id}")  # ㄴ 이러면 id로 book 가져오는거랑 겹치지 않을까
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
