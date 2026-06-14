from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    genre: str


class Member(BaseModel):
    name: str
    email: str


class WrongGenre(Exception):
    pass

class ProcessFailed(Exception):
    pass