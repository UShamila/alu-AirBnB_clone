#!/usr/bin/python3
"""
BaseModel class definition
"""
import uuid
from datetime import datetime


class BaseModel:
    """
    BaseModel class that defines all common attributes/methods for other
    classes
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize BaseModel instance
        """
        if kwargs:  # case: creating from a dictionary
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.fromisoformat(value))
                elif key != "__class__":
                    setattr(self, key, value)
            # Add to storage for instances created from dictionary
            from models import storage
            storage.new(self)
        else:  # case: creating a brand new instance
            self.id = str(uuid.uuid4())  # unique ID
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            # Add to storage for new instances
            from models import storage
            storage.new(self)

    def __str__(self):
        """String representation of the instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates the public instance attribute updated_at with current
        datetime"""
        self.updated_at = datetime.now()
        from models import storage
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__ of the
        instance"""
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict
