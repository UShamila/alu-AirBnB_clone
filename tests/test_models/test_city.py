#!/usr/bin/python3
"""
Unit tests for City class
"""
import unittest
import os
from models.city import City
from models import storage


class TestCity(unittest.TestCase):
    """Test cases for City class"""

    def setUp(self):
        """Set up test fixtures"""
        # Clear storage before each test
        storage.all().clear()
        self.city = City()

    def tearDown(self):
        """Clean up after each test"""
        # Clear storage after each test
        storage.all().clear()
        # Remove file.json if it exists
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_city_inheritance(self):
        """Test that City inherits from BaseModel"""
        from models.base_model import BaseModel
        self.assertIsInstance(self.city, BaseModel)

    def test_city_attributes(self):
        """Test City class attributes"""
        self.assertEqual(self.city.state_id, "")
        self.assertEqual(self.city.name, "")

    def test_city_attributes_assignment(self):
        """Test City attributes can be assigned"""
        self.city.state_id = "state-123"
        self.city.name = "San Francisco"
        self.assertEqual(self.city.state_id, "state-123")
        self.assertEqual(self.city.name, "San Francisco")

    def test_city_to_dict(self):
        """Test City to_dict method includes all attributes"""
        self.city.state_id = "state-123"
        self.city.name = "San Francisco"
        obj_dict = self.city.to_dict()
        
        self.assertEqual(obj_dict["__class__"], "City")
        self.assertEqual(obj_dict["state_id"], "state-123")
        self.assertEqual(obj_dict["name"], "San Francisco")

    def test_city_from_dict(self):
        """Test City creation from dictionary"""
        test_dict = {
            "id": "test-id",
            "created_at": "2023-01-01T12:00:00.000000",
            "updated_at": "2023-01-01T12:00:00.000000",
            "state_id": "state-123",
            "name": "San Francisco"
        }
        
        city = City(**test_dict)
        
        self.assertEqual(city.id, "test-id")
        self.assertEqual(city.state_id, "state-123")
        self.assertEqual(city.name, "San Francisco")

    def test_city_storage_integration(self):
        """Test City integrates with storage"""
        key = f"City.{self.city.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key], self.city)


if __name__ == '__main__':
    unittest.main()
