from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import uvicorn
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    user = secrets.compare_digest(credentials.username.encode(), b"admin")
    password = secrets.compare_digest(credentials.password.encode(), b"password")
    if not (user and password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return user
app = FastAPI()

class Author(BaseModel):
    name: str
    email: Optional[str] = None

def rating_grade(rating: float) -> str:
    if rating >= 4.0:
        return "A Rating"
    elif rating >= 3.0:
        return "B Rating"
    elif rating >= 2.0:
        return "C Rating"
    elif rating >= 1.0:
        return "D Rating"
    else:
        return "N/A Rating"

class Book(BaseModel):
    id: int
    title: str
    author: Author
    year: int
    genre: str
    rating: float

# IN-Memory Dataset!

books = [
    Book(
        id=1,
        title="The Great Gatsby",
        author= Author(name=F".Scott Fitzgerald", email="fscott@example.com"),
        year=1925,
        genre="Fiction",
        rating=5.0
    ),
    Book(
        id=2,
        title="1984",
        author=Author(name="George Orwell"),
        year=1949,
        genre="Dystopian",
        rating=4.21
    )
]


# Get all books!
@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books

#count books
@app.get("/books/count")
async def get_book_count():
    return {"Count of books": len(books)}

#Get a Book by ID
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
        raise HTTPException(status_code=404, detail="Book not found")

#Post a new books!
@app.post("/books", response_model=Book, dependencies=[Depends(verify_password)])
async def create_book(book: Book):
    if any(b.id==book.id for b in books):
        raise HTTPException(status_code=400, detail="Book ID already exists")
    books.append(book)
    return book

#PUT to update a book
@app.put("/books/{book_id}", response_model=Book, dependencies=[Depends(verify_password)])
async def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books):
        if book.id == book_id:
            books[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# DELETE a book!
@app.delete("/books/{book_id}", dependencies=[Depends(verify_password)])
async def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book.id == book_id:
            books.pop(i)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")

#Search by genre
@app.get("/books/search-genre/{genre}")
async def search_genre(genre: str):
    for book in books:
        if book.genre == genre:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

#Search by rating as-well
@app.get("/books/rating/{rating}", response_model=List[Book])
async def get_book_rating(rating: str):
    match = [b for b in books if rating_grade(b.rating) == rating.upper()]
    if not match:
        raise HTTPException(status_code=404, detail="Book not found")
    return match



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
