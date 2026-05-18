from typing import Optional

from sqlalchemy.orm import Session

from domain.models import Itinerary
from domain.ports import IItineraryRepository
from infrastructure.database import ItineraryORM, SessionLocal


class SQLiteItineraryRepository(IItineraryRepository):
    """
    Adaptador de persistencia: implementa el puerto IItineraryRepository
    usando SQLAlchemy + SQLite.
    La capa de aplicación nunca sabe que hay SQLite aquí.
    """

    def _get_session(self) -> Session:
        return SessionLocal()

    async def get_all(self) -> list[Itinerary]:
        with self._get_session() as session:
            records = session.query(ItineraryORM).all()
            return [self._to_domain(r) for r in records]

    async def get_by_id(self, itinerary_id: int) -> Optional[Itinerary]:
        with self._get_session() as session:
            record = session.query(ItineraryORM).filter(ItineraryORM.id == itinerary_id).first()
            return self._to_domain(record) if record else None

    async def create(self, itinerary: Itinerary) -> Itinerary:
        with self._get_session() as session:
            record = self._to_orm(itinerary)
            session.add(record)
            session.commit()
            session.refresh(record)
            return self._to_domain(record)

    async def update(self, itinerary_id: int, itinerary: Itinerary) -> Optional[Itinerary]:
        with self._get_session() as session:
            record = session.query(ItineraryORM).filter(ItineraryORM.id == itinerary_id).first()
            if not record:
                return None
            record.user_name = itinerary.user_name
            record.departure_airport_id = itinerary.departure_airport_id
            record.arrival_airport_id = itinerary.arrival_airport_id
            record.travel_date = itinerary.travel_date
            record.duration_minutes = itinerary.duration_minutes
            session.commit()
            session.refresh(record)
            return self._to_domain(record)

    async def delete(self, itinerary_id: int) -> bool:
        with self._get_session() as session:
            record = session.query(ItineraryORM).filter(ItineraryORM.id == itinerary_id).first()
            if not record:
                return False
            session.delete(record)
            session.commit()
            return True

    # ── Mappers ───────────────────────────────────────────────────────────────

    def _to_domain(self, record: ItineraryORM) -> Itinerary:
        return Itinerary(
            id=record.id,
            user_name=record.user_name,
            departure_airport_id=record.departure_airport_id,
            arrival_airport_id=record.arrival_airport_id,
            travel_date=record.travel_date,
            duration_minutes=record.duration_minutes,
        )

    def _to_orm(self, itinerary: Itinerary) -> ItineraryORM:
        return ItineraryORM(
            user_name=itinerary.user_name,
            departure_airport_id=itinerary.departure_airport_id,
            arrival_airport_id=itinerary.arrival_airport_id,
            travel_date=itinerary.travel_date,
            duration_minutes=itinerary.duration_minutes,
        )
