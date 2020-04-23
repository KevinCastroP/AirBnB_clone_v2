#!/usr/bin/python3

"""
Module: db__storage DB storage class
"""

from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __engine = None
    __session = None

    def __init__(self):
        """Creating engines"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.getenv("HBNB_MYSQL_USER"),
                os.getenv("HBNB_MYSQL_PWD"),
                os.getenv("HBNB_MYSQL_HOST"),
                os.getenv("HBNB_MYSQL_DB")), pool_pre_ping=True)
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        dictionary = {}
        if cls is None:
            all_cls = ["State", "City", "User", "Amenity", "Place", "Review"]
            for cl in all_cls:
                objs = self.__session.query(eval(cl))
                for obj in objs:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    dictionary[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                dictionary[key] = obj

        return dictionary

    def new(self, obj):
        """sets __object to given obj
        Args:
            obj: given object
        """
        self.__session.add(obj)

    def save(self):
        """serialize the file path to JSON file path
        """
        self.__session.commit()

    def delete(self, obj=None):
        """to delete obj from __objects if it’s inside
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload objs"""
        Base.metadata.create_all(self.__engine)
        Session_sc = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Session_sc)
        self.__session = Session()

    def close(self):
        """Calling method close to finish a session"""
        self.__session.close()
