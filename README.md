
# Library Project

"מטרת הפרויקט ##
לבנות שרת API שמנהל ספרייה,
שזה כולל ניהול הספרים וניהול מנויי הספרייה,
התקשורת עם תהיה ע"י בקשות HTTP בלבד.


תיאור השרת:##
בנוי באמצעות FAST_API
מנהל חיבור למשאב נתונים mysql
ומבצע את הפעולות הלוגיות שלו ע"י מחלקות OOP.
השרת נותן מענה לבקשות של clients דרך בקשות http
דרך זה מספק:
בקשות CRUD ומידע על המערכת.



## Installation

1. Clone the repository:
```bash
https://github.com/emg4706-Elazar/library.git
```

2. Navigate to the project directory:
```bash
cd ~/PycharmProjects/library
```

3. Install dependencies:
```bash
python -m pip install -r requirments.txt
```


## Running the project

1. Docker Setup
```bash
docker run --name library
   -e MYSQL_ROOT_PASSWORD=secret
   -e MYSQL_DATABASE=library_db
   -p 3306:3306
   -d mysql:latest
```

2. Start container
```bash
 docker start library
```

3. Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

4. Open your browser and go to:
```bash
127.0.0.1:8000/docs
```
 



## Folder Structure

```
library-api/  
│  
├── app/  
│   ├── main.py  
│   ├── database/  
│   │   ├── db\_connection.py  
│   │   ├── book\_db.py  
│   │   └── member\_db.py  
│   ├── routes/  
│   │   ├── book\_routes.py  
│   │   ├── member\_routes.py  
│   │   └── report\_routes.py  
│   └── logs/  
│       └── app.log  
│  
├── README.md  
├── requirements.txt  
└── .gitignore
```




## Database Tables

### Table: `books`

| Column name                     | Explanation                                           |
|---------------------------------|-------------------------------------------------------|
| `id`                            | primary key                                           |
| `title`                         | title book, maximum 50 chars, not null column         |
| `author`                        | auther name, maximum 50 chars, not null column        |
| `genre`                         | **values `genre` allowed:**                           |
| Fiction                         | Non-Fiction                                           | Science | History | Other — מומש כעמודת ENUM  כל ערך       |
| אחר מחזיר שגיאה , עמודה לא ריקה | במסד הנתונים,                                         |
| `is_available`                  | האם הספר זמין להשאלה — FALSE מסמן הושאל עמודה לא ריקה |
| `borrowed_by_member_id`         | מזהה החבר שמחזיק את הספר — NULL אם זמין               |



### טבלת `members` — שדות

| שדה             |                                                הסבר |
|-----------------|----------------------------------------------------:|
| `id`            |                                           מפתח ראשי |
| `name`          |            שם החבר, עמודה לא ריקה, מקסימום 50 תווים |
| `email`         |                 כתובת מייל — ייחודית, עמודה לא ריקה |
| `is_active`     |  האם החבר פעיל — FALSE לא יכול להשאיל עמודה לא ריקה |
| `total_borrows` | מונה סה"כ השאלות — עולה ב-1 בכל השאלה עמודה לא ריקה |


## python module `database`

### functions - `db_connection.py`

| פונקציה          |                                                                              תפקיד |
|------------------|-----------------------------------------------------------------------------------:|
| `get_connection` |                                         יוצר חיבור ל-MySQL — כל מחלקת DB משתמשת בה |
| `create_tables`  | יוצר את טבלאות `books` ו-`members` אם לא קיימות — רץ בעליית השרת, בתחילת פונק main |


### מחלקות OOP — `BookDB` 

אחראי על כל פעולות SQL מול טבלת `books`.

| מתודה                                       | מי קורא לה                                                              | מה היא עושה                                                                                                 |
|---------------------------------------------|-------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| `create_book(data)`                         | `POST /books`                                                           | INSERT לטבלת books — `is_available=True`, `borrowed_by=NULL`                                                |
| `get_all_books()`                           | `GET /books`                                                            | מחזירה רשימת כל הספרים                                                                                      |
| `get_book_by_id(id)`                        | `GET /books/{id}`                                                       | מחזירה ספר אחד על פי ID או None                                                                           |
| `update_book(id, data)`                     | `PUT /books/{id}`                                                       | מעדכן שדות שנשלחו                                                                                           |
| `set_available(id, val, member_id)`         | `PUT /books/{id}/return/{member_id} PUT /books/{id}/borrow/{member_id}` | מעדכן `is_available` ו-`borrowed_by_member_id`                                                              |
| `count_total_books()`                       | `GET /reports/summary`                                                  | סופר את סך כל הספרים במסד הנתונים                                                                           |
| `count_available_books()`                   | `GET /reports/summary`                                                  | סופר ספרים עם `is_available=True`                                                                           |
| `count_borrowed_books()`                    | `GET /reports/summary`                                                  | סופר ספרים עם `is_available=False`                                                                          |
| `count_by_genre(genre)`                     | `GET /reports/books-by-genre`                                           | סופר ספרים לפי ז'אנר                                                                                        |
| `count_active_borrows_by_member(member_id)` | `PUT /books/{id}/borrow/{member_id}`                                    | סופר כמה ספרים החבר מחזיק כרגע (לאכיפת חוק 7\) — ספירת books עם borrowed\_by\_member\_id השווה ל-member\_id |

## 

## מחלקות OOP — `MemberDB`

אחראי על כל פעולות SQL מול טבלת `members`.

| מתודה                     | מי קורא לה                           | מה היא עושה                                                |
|:--------------------------|:-------------------------------------|:-----------------------------------------------------------|
| `create_member(data)`     | `POST /members`                      | INSERT לטבלת members — `is_active=True`, `total_borrows=0` |
| `get_all_members()`       | `GET /members`                       | מחזירה רשימת כל החברים                                     |
| `get_member_by_id(id)`    | `GET /members/{id}`                  | מחזירה חבר אחד על פי ID או None                            |
| `update_member(id, data)` | `PUT /members/{id}`                  | מעדכן שדות שנשלחו                                          |
| `deactivate_member(id)`   | `PUT /members/{id}/deactivate`       | מעדכן `is_active=False`                                    |
| `activate_member(id)`     | `PUT /members/{id}/activate`         | מעדכן `is_active=True`                                     |
| `increment_borrows(id)`   | `PUT /books/{id}/borrow/{member_id}` | מעלה ב-1 את                                                |
| `count_active_members()`  | `GET /reports/summary`               | סופר חברים עם `is_active=True`                             |
| `get_top_member()`        | `GET /reports/top-member`            | מחזיר את החבר עם `total_borrows` הגבוה ביותר               |


## System Rules

1. **Create book** , The user `title`,`author`,`genre`,
the system add `is_available=True`, `borrowed_by=NULL`
2. **Genre** must be `Fiction` / `Non-Fiction` / `Science`
/ `History` / `Other`. Other value will return exception,
make sure that at create and put mode.
3. **Create member** , the user send `name`, `email`.
The system add `is_active=True`, `total_borrows=0`.
4. **Email** must be unique otherwise raise exception.
5. **inactive member** `is_active=False` - not allowed to borrow.
6. **Unavailable book** Not allowed a borrowed book - (`is_available=False`).
7. **max Book** A member can't hold simultaneously mor than 3 books.
8. **return book**, can be returned a book just in case,
it borrowed to a member that returns it.


## API Endpoints

### Books Endpoints

| Method | Endpoint                         | Description  | Request Body | Response |
|--------|----------------------------------|--------------|--------------|----------|
| `POST` | `/books`                         | create book  |              |          |
| `GET`  | `/books`                         | all books    |              |          |
| `GET`  | `/books/{id}`                    | book by id   |              |          |
| `PUT`  | `/books/{id}`                    | update booke |              |          |
| `PUT`  | `/books/{id}/borrow/{member_id}` | borrow book  |              |          |
| `PUT`  | `/books/{id}/return/{member_id}` | return book  |              |          |



### Members Endpoints

| Method | Endpoint                   | Description     | Request Body | Response |
|--------|----------------------------|-----------------|--------------|----------|
| `POST` | `/members`                 | create member   |              |
| `GET`  | `/members`                 | all members     |              |          |
| `GET`  | `/members/{id}`            | member by id    |              |          |
| `PUT`  | `/members/{id}`            | update member   |              |          |
| `PUT`  | `/members/{id}/deactivate` | lockout member  |              |          |
| `PUT`  | `/members/{id}/activate`   | activate member |              |          |


### Members Endpoints

| Method | Endpoint                  | Description            | Request Body | Response |
|--------|---------------------------|------------------------|--------------|----------|
| `GET`  | `/reports/summary`        | genral report          |              |          |
| `GET`  | `/reports/books-by-genre` | books by genre         |              |          |
| `GET`  | `/reports/top-member`     | The most active member |              |          |



## Flow System:

- The main module performs init to the program
- The server ready to receive requests
- The client send request to API endpoint
- THe endpoint pass it to related router
- The router call to logic functions built by OOP
- The logic functions manage connection to mysql container
- The mysql container returns the desired information.







