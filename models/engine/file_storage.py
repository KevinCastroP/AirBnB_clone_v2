#!/usr/bin/python3

"""
This module defines the FileStorage Class to AirBnB project.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import sys


class FileStorage:
    """This class serializes instances to a JSON file and"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns a dictionary returns a dictionary of __object"""
        if cls is None:
            return self.__objects
        dictionary = {}
        for i, j in self.__objects.items():
            if j.__class__ == cls:
                dictionary[i] = j
        return dictionary

    def new(self, obj):
        """sets __object to given obj given object"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """serialize the file path to JSON file path"""
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """serialize the file path to JSON file path"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """to delete obj from __objects if it’s inside"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """To deserialization the JSON file to objects"""
        self.reload()
