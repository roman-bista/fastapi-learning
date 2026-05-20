# POST request method is used to send data to the server.
# Usually for:

# creating new data
# signup/login
# adding records
# submitting forms
# ////////
# GET used to fetch/read data.  client asks server for data. "Server, give me books data."

# Example:
# @app.get("/books")
# ///////////
# POST: Used to create/send data. Client sends new data to server. "Server, save this new book."

# Example:
# @app.post("/books")
from fastapi import Body,FastAPI
app=FastAPI()

BOOKS=[
    {'title':'Tiltle One','author':'Author One','category':'science'},
    {'title':'Tiltle Two','author':'Author Two','category':'science'},
    {'title':'Tiltle Three','author':'Author Three','category':'history'},
    {'title':'Tiltle Four','author':'Author Four','category':'math'},
    {'title':'Tiltle Five','author':'Author Five','category':'math'},
    {'title':'Tiltle Six','author':'Author Two','category':'math'},

]

@app.post("/books/create_book")
async def create_book(new_book=Body()):           #Body() usually represents data entered/sent by the user or client in the request body.
    BOOKS.append(new_book)

@app.get("/books/")
async def read_all_books():
    return BOOKS



@app.get("/books/{book_title}")                              #{dynamic_pram}.   #%20 means a space ( ) in a URL.
async def read_book(book_title: str):                          #{dynamic_pram}
    for book in BOOKS:
        if book.get('title').casefold()== book_title.casefold():   #casefold() converts strings to lowercase powerful then .lower
            return book
        





# What Backend Receives

# Usually JSON:
# {
#   "name": "Roman",
#   "age": 20
# } this backend is recieving from post method yes>?