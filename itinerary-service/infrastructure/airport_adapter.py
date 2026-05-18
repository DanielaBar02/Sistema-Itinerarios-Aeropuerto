import os

import httpx

from domain.ports import IAirportValidationPort

AIRPORT_SERVICE_URL = os.getenv("AIRPORT_SERVICE_URL", "http://localhost:8000")


class AirportServiceAdapter(IAirportValidationPort):
    """
    Adaptador HTTP: implementa el puerto IAirportValidationPort
    consultando el Airport Service interno.
    
    El caso de uso nunca sabe que hay una llamada HTTP aquí.
    Si mañana se cambia a gRPC o a una función local, solo cambia este archivo.
    """

    async def airport_exists(self, airport_id: int) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{AIRPORT_SERVICE_URL}/airports/{airport_id}")
                return response.status_code == 200
        except httpx.RequestError:
            raise ConnectionError(
                "No se pudo conectar con el Airport Service. "
                "Asegúrate de que esté corriendo en el puerto 8000."
            )