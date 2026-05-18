# Sistema de Itinerarios Personales
### Arquitectura de Microservicios · Universidad Central 

---

## Descripción

Sistema web para gestionar itinerarios de viaje entre aeropuertos colombianos. Está construido sobre una arquitectura de microservicios con dos servicios independientes que se comunican entre sí, y un frontend que los consume.

---

## Tecnologías utilizadas

| Capa | Tecnología |
|---|---|
| Backend | Python 3.12 + FastAPI |
| Validación | Pydantic v2 |
| Base de datos | SQLite + SQLAlchemy |
| Frontend | HTML + Vanilla JS + Plotly JS |
| Contenerización | Docker + Docker Compose |

---

## Arquitectura

El proyecto implementa **Arquitectura Hexagonal (Ports & Adapters)** en cada microservicio. El objetivo es aislar la lógica de negocio del mundo exterior — bases de datos, APIs externas y frameworks — de manera que ninguna de esas cosas externas contamine el núcleo de la aplicación.

```
┌────────────────────────────────────────────────────────────┐
│                         FRONTEND                           │
│              index.html  +  Plotly JS                      │
└────────────┬───────────────────────┬───────────────────────┘
             │ GET /airports/map     │ CRUD /itineraries/
             ▼                       ▼
┌──────────────────────┐   ┌──────────────────────────────┐
│   AIRPORT SERVICE    │   │      ITINERARY SERVICE        │
│     puerto :8000     │◄──│  valida aeropuertos :8001    │
└──────────┬───────────┘   └──────────────┬───────────────┘
           │ HTTP                          │ SQLite
           ▼                              ▼
  ┌─────────────────┐           ┌──────────────────┐
  │   API Colombia  │           │  itineraries.db  │
  └─────────────────┘           └──────────────────┘
```

---

## Patrón Adapter

El patrón Adapter desacopla la API externa del dominio interno. `IAirportRepository` define el contrato que el resto del sistema conoce. `ApiColombiaAdapter` implementa ese contrato traduciendo la respuesta externa al modelo `Airport`. El frontend y el Itinerary Service nunca conocen la estructura de la API de Colombia.

```
IAirportRepository     ← Puerto (interfaz abstracta)
       ▲
       │ implementa
ApiColombiaAdapter     ← Adapter concreto
       │
       │ consume
api-colombia.com       ← Adaptee (API externa)
```

---

## Estructura del proyecto

```
proyecto/
├── airport-service/
│   ├── domain/
│   │   ├── models.py        ← Entidad Airport (Pydantic)
│   │   └── ports.py         ← IAirportRepository (interfaz)
│   ├── application/
│   │   └── use_cases.py     ← Lógica de negocio
│   ├── infrastructure/
│   │   └── adapter.py       ← ApiColombiaAdapter (Patrón Adapter)
│   ├── api/
│   │   └── routes.py        ← Endpoints FastAPI
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── itinerary-service/
│   ├── domain/
│   │   ├── models.py        ← Entidades Itinerary y DTOs
│   │   └── ports.py         ← IItineraryRepository, IAirportValidationPort
│   ├── application/
│   │   └── use_cases.py     ← CRUD + validación de aeropuertos
│   ├── infrastructure/
│   │   ├── database.py      ← SQLAlchemy + ORM
│   │   ├── repository.py    ← SQLiteItineraryRepository
│   │   └── airport_adapter.py ← AirportServiceAdapter (HTTP)
│   ├── api/
│   │   └── routes.py        ← Endpoints FastAPI
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   └── index.html
├── docker-compose.yml
└── README.md
```

---

## Ejecución sin Docker

Para ejecutar el proyecto necesitas tener dos terminales abiertas. En cada una entra a la carpeta del proyecto y luego a su respectivo servicio.

En la primera terminal entra a `airport-service`, instala las dependencias con `pip install -r requirements.txt` y luego inicia el servicio con `py -m uvicorn main:app --reload --port 8000`. Espera a ver el mensaje `Application startup complete` antes de continuar.

En la segunda terminal haz lo mismo pero con `itinerary-service`, usando el puerto 8001. Es importante iniciar primero el Airport Service porque el Itinerary Service lo necesita para validar los aeropuertos.

Una vez ambos estén corriendo, abre el archivo `frontend/index.html` directamente en el navegador. Si quieres revisar los endpoints disponibles, el Swagger de cada servicio está en `http://localhost:8000/docs` y `http://localhost:8001/docs`.

> **Nota:** se recomienda usar Python 3.10, 3.11 o 3.12. Python 3.13 tiene problemas de compatibilidad con algunas dependencias.

---

## Ejecución con Docker

```bash
docker-compose up --build
```

| URL | Descripción |
|---|---|
| `http://localhost:8000/docs` | Swagger Airport Service |
| `http://localhost:8001/docs` | Swagger Itinerary Service |
| `http://localhost:3000` | Frontend |

---

## Endpoints

### Airport Service (:8000)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/airports/` | Listar todos los aeropuertos |
| GET | `/airports/map` | Datos para Plotly JS |
| GET | `/airports/{id}` | Aeropuerto por ID |
| GET | `/health` | Health check |

### Itinerary Service (:8001)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/itineraries/` | Listar itinerarios |
| GET | `/itineraries/{id}` | Itinerario por ID |
| POST | `/itineraries/` | Crear itinerario |
| PUT | `/itineraries/{id}` | Actualizar itinerario |
| DELETE | `/itineraries/{id}` | Eliminar itinerario |
| GET | `/health` | Health check |
