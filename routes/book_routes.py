from fastapi import APIRouter, HTTPException
from models.models import *
from database.book_db import *
from database.member_db import *
router = APIRouter()
from logs.logging_config import logger



@router.post("/books")
def post_book(body: Book):
    logger.info("Create book started")
    body = body.model_dump()
    try:
        book_db.create_book(body)
    except WrongGenre:
        logger.error(f"Create book failed. Wrong genre: {body["genre"]}")
        raise HTTPException(status_code=409, detail="Wrong Genre")
    logger.info("New book was created successfully")
    return "book was created successfully"


@router.get("/books")
def get_books():
    if not book_db.get_all_books():
        logger.warning("Get books returned None. library is empty")
        return "The library is empty"
    logger.info("Get books performed")
    return book_db.get_all_books()


@router.get("/books/{id}")
def get_book_by_id(id: int):
    logger.info("Get book by id started")
    book = book_db.get_book_by_id(id)
    if not book:
        logger.error(f"Get book by id failed. There's no id: '{id}'")
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info("Get book by id performed")
    return book


@router.put("/books/{id}")
def put_book(id: int, data: Book):
    logger.info("Update book started")
    if not book_db.get_book_by_id(id):
        logger.error(f"Update book failed. There's no id: {id}")
        raise HTTPException(status_code=404, detail="Book not found")
    data = data.model_dump()
    try:
        book_db.update_book(id, data)
    except WrongGenre:
        logger.error(f"Update book failed. Wrong genre: {data["genre"]}")
        raise HTTPException(status_code=409, detail="Wrong Genre")
    logger.info("Update book performed")
    return "Book updated"



@router.put("/books/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id:int):
    logger.info("Borrow book stared")
    member = member_db.get_member_by_id(member_id)
    if not member:
        logger.error(f"Borrow book failed. There's no member id: {member_id}")
        raise HTTPException(status_code=404, detail="Member not found")
    if not member["is_active"]:
        logger.error(f"Borrow book failed. Member not active")
        raise HTTPException(status_code=400, detail="Member is not active")
    total_borrows = book_db.count_active_borrows_by_member(member_id)
    if total_borrows["count_active_borrows"] == 3:
        logger.error(f"Borrow book failed. Total active borrows > 3")
        raise HTTPException(status_code=400, detail="Member has reached maximum borrows")
    book = book_db.get_book_by_id(id)
    if not book:
        logger.error(f"Borrow book failed. There's no book id: {id}")
        raise HTTPException(status_code=404, detail="Book not found")
    if not book["is_available"]:
        logger.error("Borrow book failed. book not available")
        raise HTTPException(status_code=400, detail="Book is not available")
    book_db.set_available(id, False, member_id)
    member_db.increment_borrows(member_id)
    logger.info("Book was borrowed successfully")
    return "Borrow was successfully"


@router.put("/books/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    logger.info("Return book started")
    member = member_db.get_member_by_id(member_id)
    if not member:
        logger.error(f"Return book failed. There's no member id: {member_id}")
        raise HTTPException(status_code=404, detail="Member not found")
    if book_db.get_book_by_id(id)["borrowed_by_member_id"] != member_id:
        logger.error(f"Return book failed. There's no book id: {id}")
        raise HTTPException(status_code=400, detail="This book is not borrowed by you")
    book_db.set_available(id, True, None)
    logger.info(f"Book: '{id}' was returned successfully")
    return "The book was returned successfully"