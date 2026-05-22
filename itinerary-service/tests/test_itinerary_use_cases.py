import pytest
from datetime import date
from typing import Optional
from domain.models import Itinerary, ItineraryCreate, ItineraryUpdate
from domain.ports import IItineraryRepository, IAirportValidationPort
from application.use_cases import ItineraryUseCases


# ── Mocks ─────────────────────────────────────────────────────────────────────

class MockItineraryRepository(IItineraryRepository):
    """Repositorio falso en memoria para pruebas."""

    def __init__(self):
        self._store: dict[int, Itinerary] = {}
        self._next_id = 1

    async def get_all(self) -> list[Itinerary]:
        return list(self._store.values())

    async def get_by_id(self, itinerary_id: int) -> Optional[Itinerary]:
        return self._store.get(itinerary_id)

    async def create(self, itinerary: Itinerary) -> Itinerary:
        itinerary.id = self._next_id
        self._store[self._next_id] = itinerary
        self._next_id += 1
        return itinerary

    async def update(self, itinerary_id: int, itinerary: Itinerary) -> Optional[Itinerary]:
        if itinerary_id not in self._store:
            return None
        self._store[itinerary_id] = itinerary
        return itinerary

    async def delete(self, itinerary_id: int) -> bool:
        if itinerary_id not in self._store:
            return False
        del self._store[itinerary_id]
        return True


class MockAirportValidator(IAirportValidationPort):
    """Validador falso: acepta IDs del 1 al 50."""

    async def airport_exists(self, airport_id: int) -> bool:
        return 1 <= airport_id <= 50


class MockAirportValidatorAllFail(IAirportValidationPort):
    """Validador falso: todos los aeropuertos no existen."""

    async def airport_exists(self, airport_id: int) -> bool:
        return False


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def use_cases():
    return ItineraryUseCases(
        repository=MockItineraryRepository(),
        airport_validator=MockAirportValidator(),
    )


@pytest.fixture
def use_cases_airports_fail():
    return ItineraryUseCases(
        repository=MockItineraryRepository(),
        airport_validator=MockAirportValidatorAllFail(),
    )


SAMPLE_DATA = ItineraryCreate(
    user_name="Juan Pérez",
    departure_airport_id=9,
    arrival_airport_id=2,
    travel_date=date(2026, 10, 15),
    duration_minutes=90,
)


# ── Tests: create ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_crear_itinerario_exitoso(use_cases):
    itinerary = await use_cases.create(SAMPLE_DATA)
    assert itinerary.id is not None
    assert itinerary.user_name == "Juan Pérez"
    assert itinerary.departure_airport_id == 9
    assert itinerary.arrival_airport_id == 2


@pytest.mark.asyncio
async def test_crear_itinerario_aeropuerto_salida_invalido(use_cases_airports_fail):
    with pytest.raises(ValueError, match="aeropuerto de salida"):
        await use_cases_airports_fail.create(SAMPLE_DATA)


@pytest.mark.asyncio
async def test_crear_itinerario_aeropuerto_llegada_invalido():
    class ValidatorOnlyDeparture(IAirportValidationPort):
        async def airport_exists(self, airport_id: int) -> bool:
            return airport_id == 9  # Solo el de salida existe

    uc = ItineraryUseCases(
        repository=MockItineraryRepository(),
        airport_validator=ValidatorOnlyDeparture(),
    )
    with pytest.raises(ValueError, match="aeropuerto de llegada"):
        await uc.create(SAMPLE_DATA)


# ── Tests: get_all ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_all_vacio(use_cases):
    result = await use_cases.get_all()
    assert result == []


@pytest.mark.asyncio
async def test_get_all_despues_de_crear(use_cases):
    await use_cases.create(SAMPLE_DATA)
    await use_cases.create(SAMPLE_DATA)
    result = await use_cases.get_all()
    assert len(result) == 2


# ── Tests: get_by_id ──────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_by_id_existente(use_cases):
    created = await use_cases.create(SAMPLE_DATA)
    found = await use_cases.get_by_id(created.id)
    assert found is not None
    assert found.user_name == "Juan Pérez"


@pytest.mark.asyncio
async def test_get_by_id_no_existente(use_cases):
    result = await use_cases.get_by_id(999)
    assert result is None


# ── Tests: update ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_actualizar_itinerario_exitoso(use_cases):
    created = await use_cases.create(SAMPLE_DATA)
    update_data = ItineraryUpdate(user_name="Daniela Barajas")
    updated = await use_cases.update(created.id, update_data)
    assert updated.user_name == "Daniela Barajas"
    assert updated.departure_airport_id == 9


@pytest.mark.asyncio
async def test_actualizar_itinerario_no_existente(use_cases):
    update_data = ItineraryUpdate(user_name="Nadie")
    result = await use_cases.update(999, update_data)
    assert result is None


# ── Tests: delete ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_eliminar_itinerario_exitoso(use_cases):
    created = await use_cases.create(SAMPLE_DATA)
    deleted = await use_cases.delete(created.id)
    assert deleted is True


@pytest.mark.asyncio
async def test_eliminar_itinerario_no_existente(use_cases):
    deleted = await use_cases.delete(999)
    assert deleted is False


@pytest.mark.asyncio
async def test_eliminar_reduce_lista(use_cases):
    created = await use_cases.create(SAMPLE_DATA)
    await use_cases.delete(created.id)
    result = await use_cases.get_all()
    assert len(result) == 0


# ── Tests: modelo Itinerary ───────────────────────────────────────────────────

def test_duracion_negativa_invalida():
    with pytest.raises(Exception):
        Itinerary(
            user_name="Test",
            departure_airport_id=9,
            arrival_airport_id=2,
            travel_date=date(2026, 10, 15),
            duration_minutes=-10,
        )


def test_mismo_aeropuerto_invalido():
    with pytest.raises(Exception):
        Itinerary(
            user_name="Test",
            departure_airport_id=9,
            arrival_airport_id=9,
            travel_date=date(2026, 10, 15),
            duration_minutes=90,
        )
