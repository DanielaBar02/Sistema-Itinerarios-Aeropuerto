from abc import ABC, abstractmethod
from typing import Optional

from domain.models import Itinerary


class IItineraryRepository(ABC):
    """Puerto de salida: contrato para persistencia de itinerarios."""

    @abstractmethod
    async def get_all(self) -> list[Itinerary]:
        ...

    @abstractmethod
    async def get_by_id(self, itinerary_id: int) -> Optional[Itinerary]:
        ...

    @abstractmethod
    async def create(self, itinerary: Itinerary) -> Itinerary:
        ...

    @abstractmethod
    async def update(self, itinerary_id: int, itinerary: Itinerary) -> Optional[Itinerary]:
        ...

    @abstractmethod
    async def delete(self, itinerary_id: int) -> bool:
        ...


class IAirportValidationPort(ABC):
    """Puerto de salida: contrato para validar aeropuertos contra el Airport Service."""

    @abstractmethod
    async def airport_exists(self, airport_id: int) -> bool:
        ...
