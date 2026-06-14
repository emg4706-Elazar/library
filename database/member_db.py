from database.db_connection import DbConnection
from mysql.connector import IntegrityError
from models.models import *

class MemberDB:
    def __init__(self, connection: DbConnection):
        self.connection = connection

    def create_member(self, data):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO members (name, email, is_active, total_borrows)
        VALUES (%s, %s, %s, %s);
        """
        values = [data["name"], data["email"], True,0]
        try:
            cursor.execute(sql, values)
            conn.commit()
            is_created = cursor.rowcount
        finally:
            cursor.close()
            conn.close()
        if not is_created:
            raise ProcessFailed
        return

    def get_all_members(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM members;")
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        return members

    def get_member_by_id(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM members WHERE id = %s;"
        cursor.execute(sql, (id,))
        member = cursor.fetchone()
        cursor.close()
        conn.close()
        return member

    def update_member(self, id, data):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        values = [data["name"], data["email"], id]
        sql = """
        UPDATE members SET name = %s, email = %s
        WHERE id = %s;
        """
        cursor.execute(sql, values)
        is_updated = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        if not is_updated:
            raise ProcessFailed
        return

    def deactivate_member(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        sql = """
        UPDATE members SET is_active = False WHERE id = %s;
        """
        cursor.execute(sql, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return None

    def activate_member(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        sql = """
        UPDATE members SET is_active = True WHERE id = %s;
        """
        cursor.execute(sql, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return None

    def increment_borrows(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        total_borrows = self.get_member_by_id(id)["total_borrows"]
        sql = """
        UPDATE members SET total_borrows = %s WHERE id = %s;
        """
        cursor.execute(sql, (total_borrows + 1, id))
        conn.commit()
        cursor.close()
        conn.close()
        return

    def count_active_members(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
        SELECT COUNT(is_active) as active_members FROM members
        WHERE is_active = 1;
        """
        cursor.execute(sql)
        active_members = cursor.fetchone()
        cursor.close()
        conn.close()
        return active_members

    def get_top_member(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """SELECT id as member_id,
        total_borrows as borrowed
        FROM members ORDER BY total_borrows DESC
        LIMIT 1;
        """
        cursor.execute(sql)
        member = cursor.fetchone()
        cursor.close()
        conn.close()
        return member


member_db = MemberDB(DbConnection())

