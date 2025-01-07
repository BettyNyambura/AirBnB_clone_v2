#!/usr/bin/python3
""" Amenity module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ Amenity class to store amenity information """
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)

    # Many-to-Many relationship with Place using the place_amenity table
    place_amenities = relationship(
        "Place", secondary="place_amenity", backref="amenities"
    )
