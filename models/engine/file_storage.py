#!/usr/bin/python3
"""
Serializes instances to a JSON file and
deserializes JSON file to instances.
"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class_dict = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "Amenity": Amenity,
        "City": City,
        "Review": Review,
        "State": State
        }


class FileStorage:
    """The file storage engine class, that is;
    A class that serialize and deserialize instances to a JSON file
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary of objects."""
        if not cls:
            return self.__objects
        elif type(cls) == str:
            return {key: value for key, value in self.__objects.items()
                    if value.__class__.__name__ == cls}
        else:
            return {key: value for key, value in self.__objects.items()
                    if value.__class__ == cls}

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        new_dict = []
        for obj in type(self).__objects.values():
            new_dict.append(obj.to_dict())
            with open(type(self).__file_path, "w", encoding='utf-8') as file:
                json.dump(new_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects if it exists"""
        if os.path.exists(type(self).__file_path):
            try:
                with open(
                        type(self).__file_path,
                        "r", encoding="utf-8") as file:
                    obj_dict_list = json.load(file)
                    for obj_dict in obj_dict_list:
                        obj_class = class_dict[obj_dict["__class__"]]
                        obj_instance = obj_class(**obj_dict)
                        self.__objects[obj_dict["__class__"] + "." + obj_dict["id"]] = obj_instance
            except Exception as e:
                pass 

    def delete(self, obj=None):
        """ deletes an object from __objects if inside """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
                self.save()
