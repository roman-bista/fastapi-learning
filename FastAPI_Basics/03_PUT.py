# GET:Show data
# POST:Create new data
# PUT:Update existing data 

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

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold()==updated_book.get('title').casefold():
            BOOKS[i]=updated_book


