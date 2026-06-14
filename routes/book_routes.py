from fastapi import APIRouter, HTTPException
from models.models import *
from database.book_db import *
from database.member_db import *
router = APIRouter()



@router.post("/books")
def post_book(body: Book):
    body = body.model_dump()
    try:
        book_db.create_book(body)
    except WrongGenre:
        raise HTTPException(status_code=409, detail="Wrong Genre")
    return "book was created successfully"


@router.get("/books")
def get_books():
    if not book_db.get_all_books():
        return "The library is empty"
    return book_db.get_all_books()


@router.get("/books/{id}")
def get_book_by_id(id: int):
    book = book_db.get_book_by_id(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/books/{id}")
def put_book(id: int, data: Book):
    if not book_db.get_book_by_id(id):
        raise HTTPException(status_code=404, detail="Book not found")
    data = data.model_dump()
    try:
        book_db.update_book(id, data)
    except WrongGenre:
        raise HTTPException(status_code=409, detail="Wrong Genre")
    return "Book updated"



@router.put("/books/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id:int):
    member = member_db.get_member_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if not member["is_active"]:
        raise HTTPException(status_code=400, detail="Member is not active")
    total_borrows = book_db.count_active_borrows_by_member(member_id)
    if total_borrows == 3:
        raise HTTPException(status_code=400, detail="Member has reached maximum borrows")
    if not book_db.get_book_by_id(id)["is_available"]:
        raise HTTPException(status_code=400, detail="Book is not available")
    book_db.set_available(id, False, member_id)
    member_db.increment_borrows(member_id)
    return "Borrow was successfully"


@router.put("/books/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    member = member_db.get_member_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if book_db.get_book_by_id(id)["borrowed_by_member_id"] != member_id:
        raise HTTPException(status_code=400, detail="This book is not borrowed by you")
    book_db.set_available(id, True, None)
    return "The book was returned successfully"