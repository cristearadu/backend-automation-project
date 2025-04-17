from pydantic import BaseModel


class ProfileModel(BaseModel):
    name: str
