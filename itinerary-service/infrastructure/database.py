from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./itineraries.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class ItineraryORM(Base):
    """Modelo ORM: representación de la tabla en base de datos."""
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    departure_airport_id = Column(Integer, nullable=False)
    arrival_airport_id = Column(Integer, nullable=False)
    travel_date = Column(Date, nullable=False)
    duration_minutes = Column(Integer, nullable=False)


def create_tables():
    Base.metadata.create_all(bind=engine)
