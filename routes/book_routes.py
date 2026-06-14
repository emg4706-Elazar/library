from fastapi import APIRouter
from app.models.models import Book
from app.database.book_db import book_db
router = APIRouter()


@router.post("/books")
def post_book(body: Book):
    body = body.model_dump()
    book_db.create_book(body)
    return


@router.get("/books")
def get_books():
    return book_db.get_all_books()

@router.put("/books/{id}")
def put_book(id: int, data: Book):
    data = data.model_dump()
    book_db.update_book(id, data)
    return

#
# @router.get("/books/{id}")
#
#
# @router.put("/books/{id}")
#
#
# @router.put("/books/{id}/borrow/{member_id}")
#
#
# @router.put("/books/{id}/return/{member_id}")
#



