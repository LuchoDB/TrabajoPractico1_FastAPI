from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    name: str
    is_active: bool = True

class GetUsersResponse(BaseModel):
    users: List[User]


class CreateUserResponse(User):
    message:str

class DeleteUserResponse(BaseModel):
    message:str
