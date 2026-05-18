from typing import Optional

import httpx

from domain.models import Airport
from domain.ports import IAirportRepository

API_COLOMBIA_URL = "https://api-colombia.com/api/v1/Airport"


class ApiColombiaAdapter(IAirportRepository):

    async def get_all(self) -> list[Airport]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(API_COLOMBIA_URL)
            response.raise_for_status()
            raw_data = response.json()
        return [self._adapt(item) for item in raw_data if self._is_valid(item)]

    async def get_by_id(self, airport_id: int) -> Optional[Airport]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{API_COLOMBIA_URL}/{airport_id}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            raw_data = response.json()
        return self._adapt(raw_data)

    def _is_valid(self, raw: dict) -> bool:
        return (
            raw.get("latitude") is not None
            and raw.get("longitude") is not None
        )

    def _adapt(self, raw: dict) -> Airport:
        return Airport(
            id=raw["id"],
            name=raw.get("name", "Desconocido"),
            iata_code=raw.get("iataCode") or raw.get("iata_code") or "N/A",
            city=raw.get("city", {}).get("name", "Desconocida") if isinstance(raw.get("city"), dict) else raw.get("cityName", "Desconocida"),
            department=raw.get("department", {}).get("name", "Desconocido") if isinstance(raw.get("department"), dict) else raw.get("departmentName", "Desconocido"),
            latitude=float(raw["longitude"]),
            longitude=float(raw["latitude"]),
        )