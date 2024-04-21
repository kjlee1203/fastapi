from fastapi import Body, FastAPI

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
async def read_all_books():
    return BOOKS


# dynamic path parameter
# example:  http://127.0.0.1:8000/books/title%20one
# def read_book(book_title: str, new_book=Body())
# can be compiled but cause error when run.
# GET can't have a body.
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        # casefold makes everything lowercase
        if book.get("title").casefold() == book_title.casefold():
            return book


# query parameter
# example:  http://127.0.0.1:8000/books/?category=science
@app.get("/books/")  # slash at the end -> query parameter after that
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            # if the category matches the query, add it to the list
            books_to_return.append(book)
    return books_to_return


# use both.
# book_author is a path parameter, category is a query parameter
# example:  http://127.0.0.1:8000/books/author%20two/?category=science
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)

    return books_to_return


# post request (create a new book)
# example of a body: {"title": "Title Seven", "author": "Author Seven", "category": "history"}
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


# put (update) request
# example of a body: {"title": "Title Six", "author": "Author Two", "category": "history"}
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book
