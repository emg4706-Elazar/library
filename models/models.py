from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    genre: str


class ExistBook(BaseModel):
    title: str | None
    author: str | None
    genre: str| None


class Member(BaseModel):
    name: str
    email: str


class WrongGenre(Exception):
    pass

class ProcessFailed(Exception):
    pass