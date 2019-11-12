from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    BigInteger
)

Base = declarative_base()


class StartShip(Base):
    __tablename__ = 'starship'
    starship_id = Column(Integer, primary_key=True)
    name = Column(String)
    model = Column(String)
    manufacturer = Column(String)
    cost_in_credits = Column(BigInteger)
    length = Column(BigInteger)
    max_atmospheric_speed = Column(String)  # Might need to change this
    crew = Column(BigInteger)
    passengers = Column(BigInteger)
    cargo_capacity = Column(BigInteger)
    consumables = Column(String)
    hyperdrive_rating = Column(Float)
    mglt = Column(Integer)
    starship_class = Column(Integer)
    in_film_one = Column(Integer)
    in_film_two = Column(Integer)
    in_film_three = Column(Integer)
    in_film_four = Column(Integer)
    in_film_five = Column(Integer)
    in_film_six = Column(Integer)
    in_film_seven = Column(Integer)
    in_film_eight = Column(Integer)
    number_of_pilots = Column(Integer)
    created = Column(DateTime)
    edited = Column(DateTime)
    url = Column(String)

