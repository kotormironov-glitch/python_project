from typing import Annotated
from generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel

class CreateUserRequest(BaseModel):
    username: Annotated[str, CreationRule(refex=r'^[A-Za-z0-9]{3,15}$')]
    password: Annotated[str, CreationRule(refex=r'^[A-Z]{3}[a-z]{1}[0-9]{2}[!$_]{4}$')]
    role: Annotated[str, CreationRule(refex=r'^ROLE_USER')]