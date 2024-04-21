from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]


@app.get("/books")
# url 127.0.0.1:8000/books
async def read_all_books():
    return BOOKS


"""
# dynamic path parameter
# order matters. put static path first before dynamic path
@app.get("/books/{dynamic_param}")  # should match the function parameter
async def read_all_books(dynamic_param: str):
    # return whatever is passed in the dynamic path parameter
    # http://127.0.0.1:8000/books/aaaa returns {"dynamic_param": "aaaa"}
    return {"dynamic_param": dynamic_param}


# mybook is a static path parameter
# because dynamic path parameter is defined first,
# it will rerturn {"dynamic_param": mybook}.
# We should put this above the dynamic path parameter
@app.get("/books/mybook")
async def read_all_books():
    return {"book-title": "My Favorite Book"}
"""


# example:  http://127.0.0.1:8000/books/title%20one
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        # casefold makes everything lowercase
        if book.get("title").casefold() == book_title.casefold():
            return book
