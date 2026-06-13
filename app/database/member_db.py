from .db_connection import get_connection
from mysql.connector import IntegrityError

class MemberDB:
    def create_member(self, data):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO members (name, email, is_active, total_borrows)
        VALUES (%s, %s, %s, %s);
        """
        values = [data["name"], data["email"], True,0]
        try:
            cursor.execute(sql, values)
        except IntegrityError:
            return "email is not unique"
        conn.commit()
        cursor.close()
        conn.close()
        return None

    def get_all_members(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM members;")
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        return members

    def get_member_by_id(self, id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM members WHERE id = %s;"
        cursor.execute(sql, (id,))
        member = cursor.fetchone()
        cursor.close()
        conn.close()
        return member

    def  update_member(self, id, data):
        pass

    def deactivate_member(self, id):
        conn = get_connection()
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
        conn = get_connection()
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
        conn = get_connection()
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
        conn = get_connection()
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
        conn = get_connection()
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


member_db = MemberDB()

