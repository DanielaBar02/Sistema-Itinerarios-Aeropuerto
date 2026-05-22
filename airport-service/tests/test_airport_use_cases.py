import pytest
from typing import Optional
from domain.models import Airport
from domain.ports import IAirportRepository
from application.use_cases import AirportUseCases


# ── Mock del repositorio ──────────────────────────────────────────────────────

class MockAirportRepository(IAirportRepository):
    """
    Implementación falsa del puerto para pruebas.
    No llama a ninguna API externa — devuelve datos fijos.
    """

    def __init__(self, airports: list[Airport]):
        self._airports = airports

    async def get_all(self) -> list[Airport]:
        return self._airports

    async def get_by_id(self, airport_id: int) -> Optional[Airport]:
        return next((a for a in self._airports if a.id == airport_id), None)


# ── Datos de prueba ───────────────────────────────────────────────────────────

SAMPLE_AIRPORTS = [
    Airport(
        id=9,
        name="Aeropuerto Internacional José María Córdova",
        iata_code="MDE",
        city="Rionegro",
        department="Antioquia",
        latitude=6.1645,
        longitude=-75.4231,
    ),
    Airport(
        id=2,
        name="Aeropuerto Internacional Ernesto Cortissoz",
        iata_code="BAQ",
        city="Barranquilla",
        department="Atlántico",
        latitude=10.8896,
        longitude=-74.7808,
    ),
    Airport(
        id=3,
        name="Aeropuerto Internacional El Dorado",
        iata_code="BOG",
        city="Bogotá D.C.",
        department="Bogotá",
        latitude=4.7016,
        longitude=-74.1469,
    ),
]


# ── Fixture ───────────────────────────────────────────────────────────────────

@pytest.fixture
def use_cases():
    repo = MockAirportRepository(SAMPLE_AIRPORTS)
    return AirportUseCases(repository=repo)


# ── Tests: get_all_airports ───────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_all_airports_retorna_todos(use_cases):
    airports = await use_cases.get_all_airports()
    assert len(airports) == 3


@pytest.mark.asyncio
async def test_get_all_airports_retorna_tipo_correcto(use_cases):
    airports = await use_cases.get_all_airports()
    for a in airports:
        assert isinstance(a, Airport)


@pytest.mark.asyncio
async def test_get_all_airports_contiene_mde(use_cases):
    airports = await use_cases.get_all_airports()
    codigos = [a.iata_code for a in airports]
    assert "MDE" in codigos


# ── Tests: get_airport_by_id ──────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_airport_by_id_existente(use_cases):
    airport = await use_cases.get_airport_by_id(9)
    assert airport is not None
    assert airport.iata_code == "MDE"
    assert airport.city == "Rionegro"


@pytest.mark.asyncio
async def test_get_airport_by_id_no_existente_retorna_none(use_cases):
    airport = await use_cases.get_airport_by_id(999)
    assert airport is None


@pytest.mark.asyncio
async def test_get_airport_by_id_retorna_aeropuerto_correcto(use_cases):
    airport = await use_cases.get_airport_by_id(2)
    assert airport.name == "Aeropuerto Internacional Ernesto Cortissoz"
    assert airport.department == "Atlántico"


# ── Tests: get_airports_for_map ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_airports_for_map_retorna_lista(use_cases):
    result = await use_cases.get_airports_for_map()
    assert len(result) == 3


@pytest.mark.asyncio
async def test_get_airports_for_map_tiene_campos_plotly(use_cases):
    result = await use_cases.get_airports_for_map()
    for item in result:
        assert "lat" in item
        assert "lon" in item
        assert "iata_code" in item
        assert "text" in item


@pytest.mark.asyncio
async def test_get_airports_for_map_coordenadas_son_float(use_cases):
    result = await use_cases.get_airports_for_map()
    for item in result:
        assert isinstance(item["lat"], float)
        assert isinstance(item["lon"], float)


# ── Tests: modelo Airport ─────────────────────────────────────────────────────

def test_airport_model_campos_obligatorios():
    airport = Airport(
        id=1,
        name="Test",
        iata_code="TST",
        city="Ciudad",
        department="Dpto",
        latitude=4.0,
        longitude=-74.0,
    )
    assert airport.id == 1
    assert airport.iata_code == "TST"


def test_airport_model_coordenadas_negativas_validas():
    airport = Airport(
        id=1,
        name="Test",
        iata_code="TST",
        city="Ciudad",
        department="Dpto",
        latitude=-4.0,
        longitude=-74.0,
    )
    assert airport.latitude == -4.0
    assert airport.longitude == -74.0
