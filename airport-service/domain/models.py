from pydantic import BaseModel


class Airport(BaseModel):
    """Entidad de dominio: representa un aeropuerto en el sistema interno."""
    id: int
    name: str
    iata_code: str
    city: str
    department: str
    latitude: float
    longitude: float
