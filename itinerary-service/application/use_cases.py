from typing import Optional

from domain.models import Itinerary, ItineraryCreate, ItineraryUpdate
from domain.ports import IAirportValidationPort, IItineraryRepository


class ItineraryUseCases:
    """
    Capa de aplicación: orquesta el CRUD de itinerarios.
    Depende únicamente de puertos (interfaces), nunca de implementaciones concretas.
    """

    def __init__(
        self,
        repository: IItineraryRepository,
        airport_validator: IAirportValidationPort,
    ):
        self._repository = repository
        self._airport_validator = airport_validator

    async def get_all(self) -> list[Itinerary]:
        return await self._repository.get_all()

    async def get_by_id(self, itinerary_id: int) -> Optional[Itinerary]:
        return await self._repository.get_by_id(itinerary_id)

    async def create(self, data: ItineraryCreate) -> Itinerary:
        await self._validate_airports(data.departure_airport_id, data.arrival_airport_id)

        itinerary = Itinerary(
            user_name=data.user_name,
            departure_airport_id=data.departure_airport_id,
            arrival_airport_id=data.arrival_airport_id,
            travel_date=data.travel_date,
            duration_minutes=data.duration_minutes,
        )
        return await self._repository.create(itinerary)

    async def update(self, itinerary_id: int, data: ItineraryUpdate) -> Optional[Itinerary]:
        existing = await self._repository.get_by_id(itinerary_id)
        if existing is None:
            return None

        # Fusionar campos: mantener los actuales si no se envía nuevo valor
        updated = Itinerary(
            id=existing.id,
            user_name=data.user_name or existing.user_name,
            departure_airport_id=data.departure_airport_id or existing.departure_airport_id,
            arrival_airport_id=data.arrival_airport_id or existing.arrival_airport_id,
            travel_date=data.travel_date or existing.travel_date,
            duration_minutes=data.duration_minutes or existing.duration_minutes,
        )

        # Validar aeropuertos solo si cambiaron
        if data.departure_airport_id or data.arrival_airport_id:
            await self._validate_airports(
                updated.departure_airport_id,
                updated.arrival_airport_id,
            )

        return await self._repository.update(itinerary_id, updated)

    async def delete(self, itinerary_id: int) -> bool:
        return await self._repository.delete(itinerary_id)

    # ── Métodos privados ──────────────────────────────────────────────────────

    async def _validate_airports(self, departure_id: int, arrival_id: int) -> None:
        """
        Valida que ambos aeropuertos existan consultando el Airport Service.
        Lanza ValueError si alguno no existe.
        """
        departure_ok = await self._airport_validator.airport_exists(departure_id)
        if not departure_ok:
            raise ValueError(f"El aeropuerto de salida con ID {departure_id} no existe.")

        arrival_ok = await self._airport_validator.airport_exists(arrival_id)
        if not arrival_ok:
            raise ValueError(f"El aeropuerto de llegada con ID {arrival_id} no existe.")
