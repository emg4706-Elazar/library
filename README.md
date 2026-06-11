מטרת הפרויקט:
לבנות שרת API שמנהל ספרייה,
שזה כולל ניהול הספרים וניהול מנויי הספרייה,
התקשורת עם תהיה ע"י בקשות HTTP בלבד,
דרך Swagger או Postman.


תיאור השרת:
בנוי באמצעות FAST_API
מנהל חיבור למשאב נתונים mysql
ומבצע את הפעולות הלוגיות שלו ע"י מחלקות OOP.
השרת נותן מענה לבקשות של clients דרך בקשות http
דרך זה מספק:
בקשות CRUD.



מבנה תיקיות:
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





