from fastapi import APIRouter, HTTPException

from application.use_cases import ItineraryUseCases
from domain.models import Itinerary, ItineraryCreate, ItineraryUpdate
from infrastructure.airport_adapter import AirportServiceAdapter
from infrastructure.repository import SQLiteItineraryRepository

router = APIRouter(prefix="/itineraries", tags=["Itineraries"])

_use_cases = ItineraryUseCases(
    repository=SQLiteItineraryRepository(),
    airport_validator=AirportServiceAdapter(),
)


@router.get(
    "/",
    response_model=list[Itinerary],
    summary="Listar todos los itinerarios",
)
async def list_itineraries():
    return await _use_cases.get_all()


@router.get(
    "/{itinerary_id}",
    response_model=Itinerary,
    summary="Obtener itinerario por ID",
)
async def get_itinerary(itinerary_id: int):
    itinerary = await _use_cases.get_by_id(itinerary_id)
    if itinerary is None:
        raise HTTPException(status_code=404, detail=f"Itinerario {itinerary_id} no encontrado.")
    return itinerary


@router.post(
    "/",
    response_model=Itinerary,
    status_code=201,
    summary="Crear itinerario",
    description="Crea un itinerario validando que los aeropuertos existan en el Airport Service.",
)
async def create_itinerary(data: ItineraryCreate):
    try:
        return await _use_cases.create(data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.put(
    "/{itinerary_id}",
    response_model=Itinerary,
    summary="Actualizar itinerario",
)
async def update_itinerary(itinerary_id: int, data: ItineraryUpdate):
    try:
        itinerary = await _use_cases.update(itinerary_id, data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))

    if itinerary is None:
        raise HTTPException(status_code=404, detail=f"Itinerario {itinerary_id} no encontrado.")
    return itinerary


@router.delete(
    "/{itinerary_id}",
    status_code=204,
    summary="Eliminar itinerario",
)
async def delete_itinerary(itinerary_id: int):
    deleted = await _use_cases.delete(itinerary_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Itinerario {itinerary_id} no encontrado.")
