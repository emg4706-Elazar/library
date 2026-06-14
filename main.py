import uvicorn
from fastapi import FastAPI
from routes.book_routes import *
from routes.member_routes import *
from database.db_connection import *
from database.member_db import *
from routes.report_routes import *
from logs.logging_config import logger


app = FastAPI()
app.include_router(router)
logger.info("Library Management Start")
logger.info("Init app")




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

