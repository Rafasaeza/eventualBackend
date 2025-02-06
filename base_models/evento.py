from pydantic import BaseModel, Field
from bson import ObjectId

class Evento(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nombre: str
    timestamp: str
    lugar: str
    lat: float
    lon: float
    organizador: str
    imagen: str