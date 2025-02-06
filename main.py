from fastapi import FastAPI
# from backend.routers import peliculas_router, salas_router
from routers.eventos_router import router as eventos_router
from routers.usuarios_router import router as usuarios_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

#Añadir CORS
origins = [
    "https://enventual-frontend-rsa.vercel.app",
    "http://localhost:3000",  # Origen permitido
    # Añade otros orígenes si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(eventos_router, prefix="/eventos", tags=["Eventos"])
app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuarios"])
