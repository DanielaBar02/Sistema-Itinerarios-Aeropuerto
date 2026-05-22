from locust import HttpUser, task, between
import random
from datetime import date, timedelta


# ── Airport Service ───────────────────────────────────────────────────────────

class AirportServiceUser(HttpUser):
    """
    Simula usuarios consultando el Airport Service.
    Cada usuario espera entre 1 y 3 segundos entre peticiones.
    """
    host = "http://host.docker.internal:8000"
    wait_time = between(1, 3)

    @task(3)
    def listar_aeropuertos(self):
        """Tarea más frecuente: listar todos los aeropuertos."""
        self.client.get("/airports/", name="GET /airports/")

    @task(2)
    def obtener_datos_mapa(self):
        """Obtener aeropuertos en formato Plotly."""
        self.client.get("/airports/map", name="GET /airports/map")

    @task(1)
    def obtener_aeropuerto_por_id(self):
        """Obtener un aeropuerto específico por ID."""
        airport_id = random.randint(1, 50)
        self.client.get(
            f"/airports/{airport_id}",
            name="GET /airports/{id}",
        )

    @task(1)
    def health_check(self):
        """Verificar estado del servicio."""
        self.client.get("/health", name="GET /health")


# ── Itinerary Service ─────────────────────────────────────────────────────────

class ItineraryServiceUser(HttpUser):
    """
    Simula usuarios haciendo CRUD de itinerarios.
    """
    host = "http://host.docker.internal:8001"
    wait_time = between(1, 3)

    VALID_AIRPORT_IDS = [2, 3, 7, 8, 9, 11, 12, 13, 14, 16, 19, 20]

    def _random_itinerary(self) -> dict:
        """Genera un itinerario aleatorio con aeropuertos distintos."""
        ids = random.sample(self.VALID_AIRPORT_IDS, 2)
        future_date = date.today() + timedelta(days=random.randint(1, 365))
        return {
            "user_name": f"Usuario_{random.randint(1, 1000)}",
            "departure_airport_id": ids[0],
            "arrival_airport_id": ids[1],
            "travel_date": future_date.isoformat(),
            "duration_minutes": random.randint(30, 300),
        }

    @task(3)
    def listar_itinerarios(self):
        """Tarea más frecuente: listar todos los itinerarios."""
        self.client.get("/itineraries/", name="GET /itineraries/")

    @task(2)
    def crear_itinerario(self):
        """Crear un itinerario nuevo."""
        self.client.post(
            "/itineraries/",
            json=self._random_itinerary(),
            name="POST /itineraries/",
        )

    @task(1)
    def obtener_itinerario_por_id(self):
        """Obtener un itinerario específico."""
        itinerary_id = random.randint(1, 10)
        self.client.get(
            f"/itineraries/{itinerary_id}",
            name="GET /itineraries/{id}",
        )

    @task(1)
    def health_check(self):
        self.client.get("/health", name="GET /health")
