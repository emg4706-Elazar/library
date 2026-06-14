import mysql.connector



create_books_q = """
CREATE TABLE IF NOT EXISTS books (
id      INT   AUTO_INCREMENT    PRIMARY KEY,
title   VARCHAR(50)     NOT NULL,
author  VARCHAR(50)     NOT NULL,
genre   ENUM ('Fiction', 'Non-Fiction', 'Science', 'History', 'Other')  NOT NULL,
is_available    BOOLEAN   NOT NULL,
borrowed_by_member_id   INT);
"""

create_members_q = """
CREATE TABLE IF NOT EXISTS members (
id      INT   AUTO_INCREMENT    PRIMARY KEY,
name   VARCHAR(50)    NOT NULL,
email  VARCHAR(100)   NOT NULL  UNIQUE,
is_active  BOOLEAN  DEFAULT FALSE,
total_borrows  INT   NOT NULL);
"""



def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="secret",
        database="library_db"
    )

def create_tables(sql_q1, sql_q2):
    """
    received 2 queries:
    1. create 'books' table
    2. create 'member' table
    :param sql_q1:
    :param sql_q2:
    :return:
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql_q1)
    cursor.execute(sql_q2)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables(create_books_q, create_members_q)
    print("Tables was created successfully")