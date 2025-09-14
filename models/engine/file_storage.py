#!/usr/bin/python3
"""
FileStorage module for serializing and deserializing instances to/from JSON
"""
import json
import os
from datetime import datetime


class FileStorage:
    """
    FileStorage class for handling JSON serialization and deserialization
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        obj_dict = {}
        for key, obj in FileStorage.__objects.items():
            obj_dict[key] = obj.to_dict()

        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        if os.path.exists(FileStorage.__file_path):
            try:
                with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
                    obj_dict = json.load(f)

                for key, value in obj_dict.items():
                    class_name = value['__class__']
                    # Import the class dynamically
                    if class_name == 'BaseModel':
                        from models.base_model import BaseModel
                        FileStorage.__objects[key] = BaseModel(**value)
                    elif class_name == 'User':
                        from models.user import User
                        FileStorage.__objects[key] = User(**value)
                    elif class_name == 'State':
                        from models.state import State
                        FileStorage.__objects[key] = State(**value)
                    elif class_name == 'City':
                        from models.city import City
                        FileStorage.__objects[key] = City(**value)
                    elif class_name == 'Amenity':
                        from models.amenity import Amenity
                        FileStorage.__objects[key] = Amenity(**value)
                    elif class_name == 'Place':
                        from models.place import Place
                        FileStorage.__objects[key] = Place(**value)
                    elif class_name == 'Review':
                        from models.review import Review
                        FileStorage.__objects[key] = Review(**value)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
