# router/usuario_router.py
from fastapi import APIRouter, HTTPException
from base_models.usuario import Usuario
from db_connection import get_database
from datetime import datetime, timedelta
from jose import  jwt
from pydantic import BaseModel
SECRET_KEY = "secreto_super_seguro"
ALGORITHM = "HS256"
db = get_database("eventual")
logs_collection = db.get_collection("logs")
def create_token(email: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({"sub": email, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)
    return token, expiration

router = APIRouter()

class EmailRequest(BaseModel):
    email: str

@router.post("/login")
def login(data: EmailRequest):  # Esperar un objeto EmailRequest
    email = data.email
    user = logs_collection.find_one({"email": email})
    if not user:
        token, expiration = create_token(email)
        log_entry = Usuario(email=email, timestamp=datetime.utcnow(), caducidad=expiration, token=token)
        logs_collection.insert_one(log_entry.dict(by_alias=True))
    return {"message": "OK"}

@router.get("/logs")
def get_logs():
    logs = list(logs_collection.find({}, {"_id": 0, "password": 0}).sort("timestamp", -1))
    return logs
