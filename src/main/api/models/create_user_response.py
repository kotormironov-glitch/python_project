from src.main.api.models.base_model import BaseModel

class User(BaseModel):
    username: str
    role: str

class CreateUserResponse(BaseModel):
    id: int
    username: str
    password: str
    role: str