#!/usr/bin/python3
"""
Unit tests for Amenity class
"""
import unittest
import os
from models.amenity import Amenity
from models import storage


class TestAmenity(unittest.TestCase):
    """Test cases for Amenity class"""

    def setUp(self):
        """Set up test fixtures"""
        # Clear storage before each test
        storage.all().clear()
        self.amenity = Amenity()

    def tearDown(self):
        """Clean up after each test"""
        # Clear storage after each test
        storage.all().clear()
        # Remove file.json if it exists
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_amenity_inheritance(self):
        """Test that Amenity inherits from BaseModel"""
        from models.base_model import BaseModel
        self.assertIsInstance(self.amenity, BaseModel)

    def test_amenity_attributes(self):
        """Test Amenity class attributes"""
        self.assertEqual(self.amenity.name, "")

    def test_amenity_attributes_assignment(self):
        """Test Amenity attributes can be assigned"""
        self.amenity.name = "WiFi"
        self.assertEqual(self.amenity.name, "WiFi")

    def test_amenity_to_dict(self):
        """Test Amenity to_dict method includes all attributes"""
        self.amenity.name = "WiFi"
        obj_dict = self.amenity.to_dict()
        
        self.assertEqual(obj_dict["__class__"], "Amenity")
        self.assertEqual(obj_dict["name"], "WiFi")

    def test_amenity_from_dict(self):
        """Test Amenity creation from dictionary"""
        test_dict = {
            "id": "test-id",
            "created_at": "2023-01-01T12:00:00.000000",
            "updated_at": "2023-01-01T12:00:00.000000",
            "name": "WiFi"
        }
        
        amenity = Amenity(**test_dict)
        
        self.assertEqual(amenity.id, "test-id")
        self.assertEqual(amenity.name, "WiFi")

    def test_amenity_storage_integration(self):
        """Test Amenity integrates with storage"""
        key = f"Amenity.{self.amenity.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key], self.amenity)


if __name__ == '__main__':
    unittest.main()
