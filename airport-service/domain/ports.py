from abc import ABC, abstractmethod
from typing import Optional

from domain.models import Airport


class IAirportRepository(ABC):
    """Puerto de salida: contrato para obtener aeropuertos desde cualquier fuente."""

    @abstractmethod
    async def get_all(self) -> list[Airport]:
        """Retorna todos los aeropuertos disponibles."""
        ...

    @abstractmethod
    async def get_by_id(self, airport_id: int) -> Optional[Airport]:
        """Retorna un aeropuerto por su ID, o None si no existe."""
        ...
