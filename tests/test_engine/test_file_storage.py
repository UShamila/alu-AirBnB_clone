#!/usr/bin/python3
"""
Unit tests for FileStorage class
"""
import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User


class TestFileStorage(unittest.TestCase):
    """Test cases for FileStorage class"""

    def setUp(self):
        """Set up test fixtures"""
        self.storage = FileStorage()
        # Clear storage before each test
        self.storage.all().clear()
        # Remove file.json if it exists
        if os.path.exists("file.json"):
            os.remove("file.json")

    def tearDown(self):
        """Clean up after each test"""
        # Clear storage after each test
        self.storage.all().clear()
        # Remove file.json if it exists
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_all_method(self):
        """Test all method returns __objects dictionary"""
        result = self.storage.all()
        self.assertIsInstance(result, dict)
        self.assertEqual(result, FileStorage._FileStorage__objects)

    def test_new_method(self):
        """Test new method adds object to __objects"""
        base_model = BaseModel()
        self.storage.new(base_model)
        
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], base_model)

    def test_save_method(self):
        """Test save method serializes objects to JSON file"""
        base_model = BaseModel()
        self.storage.new(base_model)
        self.storage.save()
        
        self.assertTrue(os.path.exists("file.json"))
        
        with open("file.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]["__class__"], "BaseModel")
        self.assertEqual(data[key]["id"], base_model.id)

    def test_reload_method_empty_file(self):
        """Test reload method with empty file"""
        # Create empty file
        with open("file.json", "w", encoding="utf-8") as f:
            f.write("")
        
        # Should not raise exception
        self.storage.reload()

    def test_reload_method_nonexistent_file(self):
        """Test reload method with nonexistent file"""
        # Should not raise exception
        self.storage.reload()

    def test_reload_method_valid_file(self):
        """Test reload method with valid JSON file"""
        # Create test data
        base_model = BaseModel()
        base_model.name = "test_model"
        self.storage.new(base_model)
        self.storage.save()
        
        # Clear storage
        self.storage.all().clear()
        
        # Reload from file
        self.storage.reload()
        
        # Check that object was reloaded
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, self.storage.all())
        reloaded_obj = self.storage.all()[key]
        self.assertEqual(reloaded_obj.id, base_model.id)
        self.assertEqual(reloaded_obj.name, "test_model")

    def test_reload_method_invalid_json(self):
        """Test reload method with invalid JSON file"""
        # Create invalid JSON file
        with open("file.json", "w", encoding="utf-8") as f:
            f.write("invalid json content")
        
        # Should not raise exception
        self.storage.reload()

    def test_save_and_reload_cycle(self):
        """Test complete save and reload cycle"""
        # Create multiple objects
        base_model = BaseModel()
        base_model.name = "test_base"
        
        user = User()
        user.email = "test@example.com"
        user.first_name = "John"
        
        # Add to storage
        self.storage.new(base_model)
        self.storage.new(user)
        self.storage.save()
        
        # Clear storage
        self.storage.all().clear()
        
        # Reload
        self.storage.reload()
        
        # Verify objects were reloaded correctly
        base_key = f"BaseModel.{base_model.id}"
        user_key = f"User.{user.id}"
        
        self.assertIn(base_key, self.storage.all())
        self.assertIn(user_key, self.storage.all())
        
        reloaded_base = self.storage.all()[base_key]
        reloaded_user = self.storage.all()[user_key]
        
        self.assertEqual(reloaded_base.name, "test_base")
        self.assertEqual(reloaded_user.email, "test@example.com")
        self.assertEqual(reloaded_user.first_name, "John")

    def test_file_path_attribute(self):
        """Test __file_path attribute"""
        self.assertEqual(FileStorage._FileStorage__file_path, "file.json")

    def test_objects_attribute(self):
        """Test __objects attribute"""
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_multiple_instances_same_storage(self):
        """Test that multiple FileStorage instances share the same storage"""
        storage1 = FileStorage()
        storage2 = FileStorage()
        
        base_model = BaseModel()
        storage1.new(base_model)
        
        # Check that both instances see the same object
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, storage1.all())
        self.assertIn(key, storage2.all())
        self.assertEqual(storage1.all()[key], storage2.all()[key])


if __name__ == '__main__':
    unittest.main()
