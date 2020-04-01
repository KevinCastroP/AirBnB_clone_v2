#!/usr/bin/python3
"""Module: amenity
This module define Amenity class

Atributes:
    name (str): name of amenity

"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Class Amenity
    Inherits from BaseModel
    create class Amenity

    Atributes:
        name (str): name of amenity

    """
    __tablename__ = "amenities"

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ""
