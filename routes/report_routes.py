from routes.book_routes import router, HTTPException
from database.member_db import *
from database.book_db import *
from models.models import *



@router.get("/reports/summary")
def get_summary():
    summary = dict({})
    summary.update(book_db.count_total_books())
    summary.update(book_db.count_available_books())
    summary.update(book_db.count_borrowed_books())
    summary.update(member_db.count_active_members())
    return summary


@router.get("/reports/books-by-genre")
def get_by_genre(genre: str):
    if genre not in BookDB.GENRES:
        raise HTTPException(status_code=404, detail=f"Genre '{genre}' not found")
    return book_db.count_by_genre(genre)


@router.get("/reports/top-member")
def get_top_member():
    return member_db.get_top_member()