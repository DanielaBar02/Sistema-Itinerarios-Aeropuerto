from fastapi import APIRouter, HTTPException

from application.use_cases import AirportUseCases
from domain.models import Airport
from infrastructure.adapter import ApiColombiaAdapter

router = APIRouter(prefix="/airports", tags=["Airports"])

_use_cases = AirportUseCases(repository=ApiColombiaAdapter())


@router.get(
    "/",
    response_model=list[Airport],
    summary="Listar todos los aeropuertos",
    description="Retorna todos los aeropuertos colombianos adaptados desde API Colombia.",
)
async def list_airports():
    try:
        return await _use_cases.get_all_airports()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error al consultar API Colombia: {str(e)}")


@router.get(
    "/map",
    response_model=list[dict],
    summary="Datos para mapa Plotly",
    description="Retorna aeropuertos en el formato requerido por Plotly JS (lat, lon, text).",
)
async def airports_for_map():
    try:
        return await _use_cases.get_airports_for_map()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error al obtener datos del mapa: {str(e)}")


@router.get(
    "/{airport_id}",
    response_model=Airport,
    summary="Obtener aeropuerto por ID",
    description="Retorna un aeropuerto específico. Usado por el Itinerary Service para validación.",
)
async def get_airport(airport_id: int):
    try:
        airport = await _use_cases.get_airport_by_id(airport_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error al consultar API Colombia: {str(e)}")

    if airport is None:
        raise HTTPException(status_code=404, detail=f"Aeropuerto con ID {airport_id} no encontrado.")

    return airport
