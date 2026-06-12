from .db_connection import get_connection
from fastapi import HTTPException

class BookDB:
    GENRES = ["Fiction", "Non-Fiction", "Science", "History", "Other"]

    def create_book(self, data: dict):
        if data["genre"] not in BookDB.GENRES:
            raise HTTPException(status_code=400)

        conn = get_connection()
        cursor = conn.cursor()
        last_id_before = cursor.lastrowid
        sql = """
        INSERT INTO books (title, author, genre, is_available)
        VALUES (%s, %s, %s, %s);
        """
        values = [data["title"], data["author"], data["genre"], True]
        cursor.execute(sql, values)
        conn.commit()
        last_id_after = cursor.lastrowid
        cursor.close()
        conn.close()
        if last_id_before == last_id_after:
            raise HTTPException(status_code=500)
        return


    def get_all_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books;")
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        return books


    def get_book_by_id(self, id):
        """
        :param id: (int)
        :return: dict | None
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM books WHERE id = %s;"
        cursor.execute(sql, (id,))
        book = cursor.fetchone()
        cursor.close()
        conn.close()
        return book


    def update_book(self, id, data):
        """
        :param id: (int)
        :param data: (dict)
        :return:
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        values = (data["title"],
                  data["author"],
                  data["genre"],
                  id)
        sql = """UPDATE books
        SET title = %s, author = %s, genre = %s
        WHERE id = %s;
        """
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return










book_db = BookDB()
if __name__ == "__main__":

    # book_db.create_book(
    #     {
    #         "title": "The Hitchhiker's Guide to the Galaxy",
    #         "author": "Douglas Adams",
    #         "genre": "Fiction"
    #     }
    # )
    print(book_db.get_all_books())








