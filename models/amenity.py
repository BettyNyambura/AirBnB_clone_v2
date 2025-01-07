#!/usr/bin/python3
""" Amenity module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    """ Amenity class to store amenity information """
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)

    place_amenities = relationship(
        "Place", secondary="place_amenity", back_populates="amenities"
    )
