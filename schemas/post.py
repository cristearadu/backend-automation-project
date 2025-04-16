from pydantic import BaseModel


class PostModel(BaseModel):
    id: str
    title: str
    author: str


class PostPayload(BaseModel):
    title: str
    author: str
