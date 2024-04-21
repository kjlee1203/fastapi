from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field  # for validation

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):  # BaseModel, Field are from pydantic
    id: Optional[int] = None  # now we don't need to pass id in the request
    # id: Optional[int] = Field(title="ID is not needed") # not working
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)  # rating should be between 1 and 5

    # display example in the swagger, without id
    class Config:
        json_schema_extra = {
            "example": {
                "title": "A New Book",
                "author": "codingwithroby",
                "description": "A new description",
                "rating": 5,
            }
        }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5),
    Book(4, "HP1", "Author 1", "Book Description", 2),
    Book(5, "HP2", "Author 2", "Book Description", 3),
    Book(6, "HP3", "Author 3", "Book Description", 1),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


# fetch a book by id
# http://127.0.0.1:8000/books/5
@app.get("/books/{book_id}")
async def read_book(book_id: int):
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
