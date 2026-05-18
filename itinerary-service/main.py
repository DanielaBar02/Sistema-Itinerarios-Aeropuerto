from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from infrastructure.database import create_tables

app = FastAPI(
    title="Itinerary Service",
    description=(
        "Microservicio de gestión de itinerarios de viaje.\n\n"
        "Implementa un **CRUD completo** con validación de aeropuertos "
        "mediante llamadas HTTP al Airport Service. "
        "Persiste en SQLite usando SQLAlchemy con arquitectura hexagonal."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def on_startup():
    create_tables()


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "service": "itinerary-service"}
