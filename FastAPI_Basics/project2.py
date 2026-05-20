from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException, status
from  pydantic import BaseModel,Field
 
app=FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
        self.published_date=published_date


class BookRequest(BaseModel):
    id: Optional[int]= Field(description="ID is not needed on create",default=None) 
    title: str=Field(min_length=3)
    author: str= Field(min_length=1)
    description: str=Field(min_length=1, max_length=100)
    rating: int=Field(gt=-1,lt=6)
    published_date: int=Field(gt=1999, lt=2031)

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
 
BOOKS=[
    Book(1, 'comp science pro', 'coding with ruby', ' a very nice book!',5, 2020),
    Book(2, 'be fast with fastapi','coding with ruby', ' a great book!',5, 2028),
    Book(3, 'master endpoints','coding with ruby', ' a awsome book !',5, 2027),
    Book(4, 'HP1','author 1', ' a very nice book!',2, 2026),
    Book(5, 'HP2','author 2', ' a very nice book!',3, 2001),
    Book(6, 'HP3','Author 3', '  description book!',1, 2029)
]

@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)        #path
async def read_book(book_id: int= Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="item not found")

@app.get("/books/",status_code=status.HTTP_200_OK)     #query
async def read_book_by_rating(book_rating: int=Query(gt=0, lt=6)):
    filtered_book=[]
    for book in BOOKS:
        if book.rating == book_rating:
            filtered_book.append(book)
    return filtered_book

@app.get("/books/publish/", status_code=status.HTTP_200_OK)         #query
async def read_books_by_publish_date(published_date: int = Query(gt=1999, lt=2031)):
    filtered_books = []

    for i in range(len(BOOKS)):
        if BOOKS[i].published_date == published_date:
            filtered_books.append(BOOKS[i])

    return filtered_books

@app.post("/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i]=book
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail="item didnot found.")
    

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int= Path(gt=0)):
    book_changed=False

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id: 
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="item didnot found.")

def find_book_id(book: Book):                       #The parameter "book" should be a Book object
   book.id= 1 if len(BOOKS)==0 else BOOKS[-1].id + 1
   return book

    # if len(BOOKS)>0:
    #     book.id=BOOKS[-1].id+1
    # else:
    #     book.id=1
    # return book

# /////////   /////////////   //////////////
# Pydantic is a Python library used for data validation, parsing, and settings management using Python type hints.
# /////////////////////////////////   /   /