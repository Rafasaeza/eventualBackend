# router/evento_router.py
from fastapi import APIRouter, HTTPException, Query
from typing import List
from base_models.evento import Evento
from db_connection import get_database
from bson import ObjectId

router = APIRouter()
db = get_database("eventual")
eventos_collection = db.get_collection("eventos")

@router.post("/", response_model=Evento)
def create_evento(evento: Evento):
    evento_dict = evento.dict(by_alias=True)
    eventos_collection.insert_one(evento_dict)
    return evento

@router.get("/", response_model=List[Evento])
def get_eventos(lat: float = Query(None), lon: float = Query(None)):
    query = {}
    if lat and lon:
        query = {"lat": {"$gte": lat - 0.2, "$lte": lat + 0.2}, "lon": {"$gte": lon - 0.2, "$lte": lon + 0.2}}
    eventos = list(eventos_collection.find(query))
    return eventos

@router.get("/{evento_id}", response_model=Evento)
def get_evento(evento_id: str):
    evento = eventos_collection.find_one({"_id": evento_id})
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento

@router.put("/{evento_id}", response_model=Evento)
def update_evento(evento_id: str, evento: Evento):
    eventos_collection.update_one({"_id": evento_id}, {"$set": evento.dict(by_alias=True)})
    return evento

@router.delete("/{evento_id}")
def delete_evento(evento_id: str):
    eventos_collection.delete_one({"_id": evento_id})
    return {"message": "Evento eliminado"}
