#!/usr/bin/python3
"""
Unit tests for BaseModel class
"""
import unittest
import os
import json
from datetime import datetime
from models.base_model import BaseModel
from models import storage


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def setUp(self):
        """Set up test fixtures"""
        # Clear storage before each test
        storage.all().clear()
        self.base_model = BaseModel()

    def tearDown(self):
        """Clean up after each test"""
        # Clear storage after each test
        storage.all().clear()
        # Remove file.json if it exists
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_init_without_args(self):
        """Test BaseModel initialization without arguments"""
        self.assertIsInstance(self.base_model, BaseModel)
        self.assertIsInstance(self.base_model.id, str)
        self.assertIsInstance(self.base_model.created_at, datetime)
        self.assertIsInstance(self.base_model.updated_at, datetime)
        self.assertIsNotNone(self.base_model.id)

    def test_init_with_kwargs(self):
        """Test BaseModel initialization with keyword arguments"""
        test_dict = {
            "id": "test-id",
            "created_at": "2023-01-01T12:00:00.000000",
            "updated_at": "2023-01-01T12:00:00.000000",
            "name": "test_name",
            "value": 42
        }
        base_model = BaseModel(**test_dict)
        
        self.assertEqual(base_model.id, "test-id")
        self.assertEqual(base_model.name, "test_name")
        self.assertEqual(base_model.value, 42)
        self.assertIsInstance(base_model.created_at, datetime)
        self.assertIsInstance(base_model.updated_at, datetime)

    def test_init_with_class_key(self):
        """Test BaseModel initialization ignores __class__ key"""
        test_dict = {
            "id": "test-id",
            "__class__": "SomeClass",
            "name": "test_name"
        }
        base_model = BaseModel(**test_dict)
        
        self.assertEqual(base_model.id, "test-id")
        self.assertEqual(base_model.name, "test_name")
        # __class__ is a built-in Python attribute, so it will always exist
        # but it should be the actual class, not the value from kwargs
        self.assertEqual(base_model.__class__.__name__, "BaseModel")

    def test_str_representation(self):
        """Test string representation of BaseModel"""
        expected = f"[BaseModel] ({self.base_model.id}) {self.base_model.__dict__}"
        self.assertEqual(str(self.base_model), expected)

    def test_save_method(self):
        """Test save method updates updated_at"""
        old_updated_at = self.base_model.updated_at
        self.base_model.save()
        self.assertGreater(self.base_model.updated_at, old_updated_at)

    def test_to_dict_method(self):
        """Test to_dict method returns correct dictionary"""
        obj_dict = self.base_model.to_dict()
        
        self.assertIsInstance(obj_dict, dict)
        self.assertIn("__class__", obj_dict)
        self.assertIn("id", obj_dict)
        self.assertIn("created_at", obj_dict)
        self.assertIn("updated_at", obj_dict)
        
        self.assertEqual(obj_dict["__class__"], "BaseModel")
        self.assertEqual(obj_dict["id"], self.base_model.id)
        self.assertIsInstance(obj_dict["created_at"], str)
        self.assertIsInstance(obj_dict["updated_at"], str)

    def test_to_dict_datetime_format(self):
        """Test to_dict method formats datetime correctly"""
        obj_dict = self.base_model.to_dict()
        created_at_str = obj_dict["created_at"]
        updated_at_str = obj_dict["updated_at"]
        
        # Check ISO format
        self.assertRegex(created_at_str, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}')
        self.assertRegex(updated_at_str, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}')

    def test_unique_ids(self):
        """Test that each instance has a unique ID"""
        base_model1 = BaseModel()
        base_model2 = BaseModel()
        
        self.assertNotEqual(base_model1.id, base_model2.id)

    def test_storage_integration(self):
        """Test that BaseModel integrates with storage"""
        # Check that the instance is added to storage
        key = f"BaseModel.{self.base_model.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key], self.base_model)

    def test_save_updates_storage(self):
        """Test that save method updates storage"""
        # Clear storage first
        storage.all().clear()
        
        # Create new instance
        base_model = BaseModel()
        base_model.save()
        
        # Check that it's in storage
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, storage.all())


if __name__ == '__main__':
    unittest.main()
