from routes.book_routes import router, HTTPException
from database.member_db import *
from database.book_db import *
from models.models import *
from logs.logging_config import logger


@router.get("/reports/summary")
def get_summary():
    logger.info("Get_summary started")
    summary = dict({})
    summary.update(book_db.count_total_books())
    summary.update(book_db.count_available_books())
    summary.update(book_db.count_borrowed_books())
    summary.update(member_db.count_active_members())
    logger.info("Get summary performed")
    return summary


@router.get("/reports/books-by-genre")
def get_by_genre(genre: str):
    logger.info("Get by genre started")
    if genre not in BookDB.GENRES:
        logger.error(f"Wrong Genre: '{genre}'")
        raise HTTPException(status_code=404, detail=f"Genre '{genre}' not found")
    logger.info("Get by genre performed")
    return book_db.count_by_genre(genre)


@router.get("/reports/top-member")
def get_top_member():
    logger.info("Get top member performed")
    return member_db.get_top_member()