#!/usr/bin/python3
"""
Unit tests for Place class
"""
import unittest
import os
from models.place import Place
from models import storage


class TestPlace(unittest.TestCase):
    """Test cases for Place class"""

    def setUp(self):
        """Set up test fixtures"""
        # Clear storage before each test
        storage.all().clear()
        self.place = Place()

    def tearDown(self):
        """Clean up after each test"""
        # Clear storage after each test
        storage.all().clear()
        # Remove file.json if it exists
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_place_inheritance(self):
        """Test that Place inherits from BaseModel"""
        from models.base_model import BaseModel
        self.assertIsInstance(self.place, BaseModel)

    def test_place_attributes(self):
        """Test Place class attributes"""
        self.assertEqual(self.place.city_id, "")
        self.assertEqual(self.place.user_id, "")
        self.assertEqual(self.place.name, "")
        self.assertEqual(self.place.description, "")
        self.assertEqual(self.place.number_rooms, 0)
        self.assertEqual(self.place.number_bathrooms, 0)
        self.assertEqual(self.place.max_guest, 0)
        self.assertEqual(self.place.price_by_night, 0)
        self.assertEqual(self.place.latitude, 0.0)
        self.assertEqual(self.place.longitude, 0.0)
        self.assertEqual(self.place.amenity_ids, [])

    def test_place_attributes_assignment(self):
        """Test Place attributes can be assigned"""
        self.place.city_id = "city-123"
        self.place.user_id = "user-123"
        self.place.name = "Cozy Apartment"
        self.place.description = "A beautiful apartment"
        self.place.number_rooms = 2
        self.place.number_bathrooms = 1
        self.place.max_guest = 4
        self.place.price_by_night = 100
        self.place.latitude = 37.7749
        self.place.longitude = -122.4194
        self.place.amenity_ids = ["amenity-1", "amenity-2"]
        
        self.assertEqual(self.place.city_id, "city-123")
        self.assertEqual(self.place.user_id, "user-123")
        self.assertEqual(self.place.name, "Cozy Apartment")
        self.assertEqual(self.place.description, "A beautiful apartment")
        self.assertEqual(self.place.number_rooms, 2)
        self.assertEqual(self.place.number_bathrooms, 1)
        self.assertEqual(self.place.max_guest, 4)
        self.assertEqual(self.place.price_by_night, 100)
        self.assertEqual(self.place.latitude, 37.7749)
        self.assertEqual(self.place.longitude, -122.4194)
        self.assertEqual(self.place.amenity_ids, ["amenity-1", "amenity-2"])

    def test_place_to_dict(self):
        """Test Place to_dict method includes all attributes"""
        self.place.name = "Cozy Apartment"
        self.place.number_rooms = 2
        self.place.price_by_night = 100
        obj_dict = self.place.to_dict()
        
        self.assertEqual(obj_dict["__class__"], "Place")
        self.assertEqual(obj_dict["name"], "Cozy Apartment")
        self.assertEqual(obj_dict["number_rooms"], 2)
        self.assertEqual(obj_dict["price_by_night"], 100)

    def test_place_from_dict(self):
        """Test Place creation from dictionary"""
        test_dict = {
            "id": "test-id",
            "created_at": "2023-01-01T12:00:00.000000",
            "updated_at": "2023-01-01T12:00:00.000000",
            "city_id": "city-123",
            "user_id": "user-123",
            "name": "Cozy Apartment",
            "number_rooms": 2,
            "price_by_night": 100
        }
        
        place = Place(**test_dict)
        
        self.assertEqual(place.id, "test-id")
        self.assertEqual(place.city_id, "city-123")
        self.assertEqual(place.user_id, "user-123")
        self.assertEqual(place.name, "Cozy Apartment")
        self.assertEqual(place.number_rooms, 2)
        self.assertEqual(place.price_by_night, 100)

    def test_place_storage_integration(self):
        """Test Place integrates with storage"""
        key = f"Place.{self.place.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key], self.place)


if __name__ == '__main__':
    unittest.main()
