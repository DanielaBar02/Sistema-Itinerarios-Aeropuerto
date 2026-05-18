from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

app = FastAPI(
    title="Airport Service",
    description=(
        "Microservicio de aeropuertos colombianos.\n\n"
        "Implementa el **patrón Adapter** para desacoplar la API externa (API Colombia) "
        "del modelo de dominio interno. El frontend y el Itinerary Service solo conocen "
        "el contrato interno, nunca la estructura de la API externa."
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


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "service": "airport-service"}
