from fastapi import FastAPI
app = FastAPI()                           #Create FastAPI application and store in app variable: car = Car()

books = [
    {"title": "title one",   "author": "author one",     "category": "science"},
    {"title": "title two",   "author": "author two",    "category": "comp"},
    {"title": "title three", "author": "author three",  "category": "math"},
    {"title": "title four",  "author": "author four",   "category": "social"},
    {"title": "title five",  "author": "author five",   "category": "science"},
    {"title": "title six",  "author": "author six",   "category": "science"},
]

@app.get("/api-endpoint")
async def first_api():
    return {"message": "hello roman"}

@app.get("/books")
async def read_all_books():
    return books  

# uvicorn module_name:variable_name

 
# path parameter: path parameter is a value passed directly in the URL path. 
# we have two parameter: static and dynamic where static route is fixed and dynamic contains a variable value eg /users/{user_id} 


# @app.get("/books/{dynamic_param}")  url:127.10.0.01:8000/boks/book_one
# async def read_all_books(dynamic_pram):
#     return {'dynamic_param': dynamic_pram}  

@app.get("/books/{book_title}")     #{dynamic_pram}.   #%20 means a space ( ) in a URL.
async def read_book(book_title: str):            #{dynamic_pram}
    for book in books:
        if book.get('title').casefold()== book_title.casefold():   #casefold() converts strings to lowercase powerful then .lower
            return book
        

@app.get("/books/{dynamic_pram}")     #{dynamic_pram}
async def read_all_books(dynamic_pram: str):
    return {"dynamic_pram":dynamic_pram}


# @app.get("/books/mybook")
# async def read_all_books():
#     return {"book_title":"my favourite book"}
 


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

# query parameter. : query parameters are values passed in the URL after a ?
# They are mainly used for:
# filtering
# searching
# sorting
# pagination
# optional values

# @app.get("/books/")
# async def read_category_by_query(category: str):
#     books_to_return=[]
#     for book in books:
#         if book.get('category').casefold()==category.casefold():
#             books_to_return.append(book)
#     return books_to_return



@app.get("/books/")
async def read_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in books:
        if book.get('author').casefold() == book_author.casefold() and book.get("category").casefold()==category.casefold():
            books_to_return.append(book)
    return books_to_return

# @app.get("/books/{book_author}/")
# async def read_category_by_query(book_author: str, category: str):
#     books_to_return=[]
#     for book in books:
#         if book.get('author').casefold() == book_author.casefold() and book.get("category").casefold()==category.casefold():
#             books_to_return.append(book)
#     return books_to_return

@app.get("/try/")
async def read_by_query(category: str):
    filtered_book=[]
    for book in books:
        if book.get("category").casefold()==category.casefold():
            filtered_book.append(book)
    return filtered_book 

# note GET donot have any body
# async=Start cooking
# while waiting,
# handle another order
# GET Request:Usually uses data already stored on the server and sends/displays it to the user/client.