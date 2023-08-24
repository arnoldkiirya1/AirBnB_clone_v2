#!/usr/bin/python3
  2 """
  3 Serializes instances to a JSON file and
  4 deserializes JSON file to instances.
  5 """
  6 
  7 import json
  8 import os
  9 from models.base_model import BaseModel
 10 from models.user import User
 11 from models.place import Place
 12 from models.state import State
 13 from models.city import City
 14 from models.amenity import Amenity
 15 from models.review import Review
 16 
 17 class_dict = {
 18     "BaseModel": BaseModel,
 19     "User": User,
 20     "Place": Place,
 21     "Amenity": Amenity,
 22     "City": City,
 23     "Review": Review,
 24     "State": State
 25 }
 26 
 27 
 28 class FileStorage:
 29     """The file storage engine class, that is;
 30     A class that serialize and deserialize instances to a JSON file
 31     """
 32     __file_path = "file.json"
 33     __objects = {}
 34 
 35     def all(self, cls=None):
 36         """Returns the dictionary of objects."""
 37         if not cls:
 38             return self.__objects
 39         elif type(cls) == str:
 40             return {key: value for key, value in self.__objects.items()
 41                     if value.__class__.__name__ == cls}
 42         else:
 43             return {key: value for key, value in self.__objects.items()
 44                     if value.__class__ == cls}
 45 
 46     def new(self, obj):
 47         """Adds new object to storage dictionary"""
 48         self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj
 49 
 50     def save(self):
 51         """serializes __objects to the JSON file (path: __file_path)"""
 52         new_dict = []
 53         for obj in type(self).__objects.values():
 54             new_dict.append(obj.to_dict())
 55         with open(type(self).__file_path, "w", encoding='utf-8') as file:
 56             json.dump(new_dict, file)
 57 
 58     def reload(self):
 59         """Deserializes the JSON file to __objects if it exists"""
 60         if os.path.exists(type(self).__file_path):
 61             try:
 62                 with open(type(self).__file_path, "r", encoding="utf-8") as file:
 63                     obj_dict_list = json.load(file)
 64                     for obj_dict in obj_dict_list:
 65                         obj_class = class_dict[obj_dict["__class__"]]
 66                         obj_instance = obj_class(**obj_dict)
 67                         self.__objects[obj_dict["__class__"] + "." + obj_dict["id"]] = obj_ins    tance
 68             except Exception as e:
 69                 pass  # Handle exceptions appropriately based on your needs
 70 
 71     def delete(self, obj=None):
 72         """ deletes an object from __objects if inside """
 73         if obj is not None:
 74             key = "{}.{}".format(obj.__class__.__name__, obj.id)
 75             if key in self.__objects:
 76                 del self.__objects[key]
 77                 self.save()
