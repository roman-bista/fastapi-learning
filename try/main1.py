from fastapi import FastAPI, HTTPException,Query
from pydantic import BaseModel,Field
from starlette import status

app=FastAPI()

BOOKS = [
    {"id": 1, "title": "Atomic Habits", "author": "James Clear", "genre": "Self Improvement", "rating": 4.8},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin", "genre": "Programming", "rating": 4.7},
    {"id": 3, "title": "Deep Work", "author": "Cal Newport", "genre": "Productivity", "rating": 4.6},
    {"id": 4, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "genre": "Software Engineering", "rating": 4.9},
    {"id": 5, "title": "Rich Dad Poor Dad", "author": "Robert Kiyosaki", "genre": "Finance", "rating": 4.5}
]
class Book(BaseModel):
    id: int=Field(gt=0)
    title: str
    author: str
    genre: str
    rating:float=Field(gt=0, le=5)
model_config = {
    "json_schema_extra": {
        "example": {
            "title": "a new book",
            "author": "henry mart",
            "description": "a new description",
            "rating": 3,
            "published_date": 2000
        }
    }
}

# @app.get("/books/")
# async def read_all_books():
#     return BOOKS

# @app.get("/books/{book_id}")
# async def read_book_by_id(book_id: int):
#     for book in BOOKS:
#         if book["id"] == book_id:
#             return book

#     raise HTTPException(
#         status_code=404,
#         detail="Book not found"
#     )
@app.post("/books/")
async def create_book(book: Book):
    book_model=book.model_dump()
    BOOKS.append(book_model)
    return book_model

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: Book):
    book_changed = False

    for i in range(len(BOOKS)):
        if BOOKS[i]["id"] == book.id:
            BOOKS[i] = book.model_dump()
            book_changed = True

    if not book_changed:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
@app.delete("/books/{book_id}")
async def delete_book_by_id(book_id: int,):
    for i in range(len(BOOKS)):
        if BOOKS[i]["id"]==book_id:
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="book not found")

# now query
# @app.get("/books/")
# async def search_by_book_id(book_id: int):
#     filtered_books=[]
#     for book in BOOKS:
#         if book["id"]==book_id:
#             filtered_books.append(book)
#     return filtered_books

@app.get("/books/")
async def search_books(
    book_id: int = None,
    author_name: str = None
):

    filtered_books = []

    for book in BOOKS:

        if book_id is not None and book["id"] != book_id:
            continue

        if author_name is not None and book["author"] != author_name:
            continue

        filtered_books.append(book)

    return filtered_books

@app.get("/books/")
async def search_book_by_rating(rating: float = Query(gt=0, le=5)):
    filtered_books=[]
    for book in BOOKS:
        if book['rating']==rating:
            filtered_books.append(book)
    return filtered_books