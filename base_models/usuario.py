# base_model/Usuario.py
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from datetime import datetime

class Usuario(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    email: EmailStr
    timestamp: datetime
    caducidad: datetime
    token: str
