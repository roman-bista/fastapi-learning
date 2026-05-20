# get all books from a specific author using path or query parameters
from fastapi import FastAPI
app=FastAPI()

BOOKS = [
    {"title": "title one",   "author": "author one",     "category": "science"},
    {"title": "title two",   "author": "author two",    "category": "comp"},
    {"title": "title three", "author": "author three",  "category": "math"},
    {"title": "title four",  "author": "author four",   "category": "social"},
    {"title": "title five",  "author": "author five",   "category": "science"},
    {"title": "title six",  "author": "author six",   "category": "science"},
]



@app.get("/books/byauthor/{author}")                #this is path parameter usually inside {}and its URL /books/roman
async def read_by_author(author: str):              #/book/ after ? and its URL /books/?author=Roman this is query
    books_to_return=[]
    for i in BOOKS:
        if i.get('author').casefold()==author.casefold():
            books_to_return.append(i)

    return books_to_return

# /////////   //////////  //////////  ///////////
# In FastAPI, route order matters because FastAPI checks routes from top to bottom.


# @app.get("/books/mybook"). 1st order
# async def my_book():
#     return {"book": "My Favorite Book"}


# @app.get("/books/{book_name}").  2nd order 
# async def get_book(book_name: str):
#     return {"book": book_name}