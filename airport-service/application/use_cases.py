from typing import Optional

from domain.models import Airport
from domain.ports import IAirportRepository


class AirportUseCases:
    """
    Capa de aplicación: orquesta la lógica de negocio.
    Solo depende del puerto (interfaz), nunca de la implementación concreta.
    """

    def __init__(self, repository: IAirportRepository):
        self._repository = repository

    async def get_all_airports(self) -> list[Airport]:
        """Obtiene todos los aeropuertos colombianos."""
        return await self._repository.get_all()

    async def get_airport_by_id(self, airport_id: int) -> Optional[Airport]:
        """Obtiene un aeropuerto específico por ID."""
        return await self._repository.get_by_id(airport_id)

    async def get_airports_for_map(self) -> list[dict]:
        """
        Transforma los aeropuertos al formato requerido por Plotly JS.
        Esta transformación es responsabilidad de la capa de aplicación.
        """
        airports = await self._repository.get_all()
        return [
            {
                "id": a.id,
                "name": a.name,
                "iata_code": a.iata_code,
                "city": a.city,
                "department": a.department,
                "lat": a.latitude,
                "lon": a.longitude,
                "text": f"{a.name} ({a.iata_code})<br>{a.city}, {a.department}",
            }
            for a in airports
        ]
