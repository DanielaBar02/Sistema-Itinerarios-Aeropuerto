from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator


class Itinerary(BaseModel):
    """Entidad de dominio: representa un itinerario de viaje."""
    id: Optional[int] = None
    user_name: str
    departure_airport_id: int
    arrival_airport_id: int
    travel_date: date
    duration_minutes: int

    @field_validator("duration_minutes")
    @classmethod
    def duration_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("La duracion debe ser mayor a 0 minutos.")
        return v

    @field_validator("arrival_airport_id")
    @classmethod
    def airports_must_differ(cls, v: int, info) -> int:
        departure = info.data.get("departure_airport_id")
        if departure is not None and v == departure:
            raise ValueError("El aeropuerto de llegada debe ser diferente al de salida.")
        return v

    @field_validator("travel_date")
    @classmethod
    def date_must_be_future(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("La fecha de viaje no puede ser una fecha pasada.")
        return v


class ItineraryCreate(BaseModel):
    """DTO de entrada para crear un itinerario."""
    user_name: str
    departure_airport_id: int
    arrival_airport_id: int
    travel_date: date
    duration_minutes: int

    @field_validator("travel_date")
    @classmethod
    def date_must_be_future(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("La fecha de viaje no puede ser una fecha pasada.")
        return v


class ItineraryUpdate(BaseModel):
    """DTO de entrada para actualizar un itinerario (todos los campos opcionales)."""
    user_name: Optional[str] = None
    departure_airport_id: Optional[int] = None
    arrival_airport_id: Optional[int] = None
    travel_date: Optional[date] = None
    duration_minutes: Optional[int] = None

    @field_validator("travel_date")
    @classmethod
    def date_must_be_future(cls, v: date) -> date:
        if v is not None and v < date.today():
            raise ValueError("La fecha de viaje no puede ser una fecha pasada.")
        return v
