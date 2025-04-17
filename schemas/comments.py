from pydantic import BaseModel


class CommentModel(BaseModel):
    id: str
    body: str
    postId: str


class CommentPayload(BaseModel):
    body: str
    postId: str
