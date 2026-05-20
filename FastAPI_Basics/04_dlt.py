# Simple HTTP Method Flow::

# Method	   Purpose
# GET	       Read data
# POST	   Create data
# PUT	       Update data
# DELETE	   Remove data


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

@app.get("/books/")
async def read_all_books():
    return BOOKS


@app.delete("/books/{book_title}")
async def delete_book(book_title: str):

    for i in range(len(BOOKS)):

        if BOOKS[i].get("title").casefold() == book_title.casefold():

            BOOKS.pop(i)

            break

    return BOOKS