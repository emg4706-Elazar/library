from .db_connection import get_connection
class BookDB:
    GENRES = ["Fiction", "Non-Fiction", "Science", "History", "Other"]

    def create_book(self, data: dict):
        if data["genre"] not in BookDB.GENRES:
            return "WrongGenre"

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
            return "ProcessFailed"
        return None

    def get_all_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books;")
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        return books

    def get_book_by_id(self, id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM books WHERE id = %s;"
        cursor.execute(sql, (id,))
        book = cursor.fetchone()
        cursor.close()
        conn.close()
        return book

    def update_book(self, id, data):
        if data["genre"] not in BookDB.GENRES:
            return "WrongGenre"
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

    def set_available(self, id, val, member_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
        UPDATE books SET is_available = %s,
        borrowed_by_member_id = %s WHERE id = %s;
        """
        cursor.execute(sql, (val, member_id, id))
        conn.commit()
        cursor.close()
        conn.close()
        return

    def count_total_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
        SELECT COUNT(*) as total_books FROM books;
        """
        cursor.execute(sql)
        total = cursor.fetchone()
        cursor.close()
        conn.close()
        return total

    def count_available_books(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
        SELECT COUNT(is_available) as available_books FROM books
        WHERE is_available = 1;
        """
        cursor.execute(sql)
        available_books = cursor.fetchone()
        cursor.close()
        conn.close()
        return available_books

    def count_borrowed_books(self):
        pass

    def count_by_genre(self, genre):
        pass

    def count_active_borrows_by_member(self, member_id):
        pass



book_db = BookDB()
if __name__ == "__main__":
    book_db = BookDB()









