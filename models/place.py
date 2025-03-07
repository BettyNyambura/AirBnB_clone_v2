#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


# Linking table for Many-to-Many relationship between Place and Amenity
place_amenity = Table(
    'place_amenity', Base.metadata,
    Column(
        'place_id', String(60), ForeignKey('places.id'),
        primary_key=True, nullable=False
    ),
    Column(
        'amenity_id', String(60), ForeignKey('amenities.id'),
        primary_key=True, nullable=False
    )
)

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    reviews = relationship(
        "Review", backref="place", cascade="all, delete, delete-orphan"
    )

     # DBStorage relationship
    amenities = relationship(
        "Amenity", secondary=place_amenity, viewonly=False
    )

    # For FileStorage, the getter and setter for amenities are added below
    @property
    def amenities(self):
        return [
            models.storage.get(Amenity, amenity_id)
            for amenity_id in self.amenity_ids
        ]

    @amenities.setter
    def amenities(self, obj):
        if isinstance(obj, Amenity):
            self.amenity_ids.append(obj.id)
