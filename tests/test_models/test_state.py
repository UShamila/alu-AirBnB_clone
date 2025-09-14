#!/usr/bin/python3
"""
Unit tests for State class
"""
import unittest
import os
from models.state import State
from models import storage


class TestState(unittest.TestCase):
    """Test cases for State class"""

    def setUp(self):
        """Set up test fixtures"""
        # Clear storage before each test
        storage.all().clear()
        self.state = State()

    def tearDown(self):
        """Clean up after each test"""
        # Clear storage after each test
        storage.all().clear()
        # Remove file.json if it exists
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_state_inheritance(self):
        """Test that State inherits from BaseModel"""
        from models.base_model import BaseModel
        self.assertIsInstance(self.state, BaseModel)

    def test_state_attributes(self):
        """Test State class attributes"""
        self.assertEqual(self.state.name, "")

    def test_state_attributes_assignment(self):
        """Test State attributes can be assigned"""
        self.state.name = "California"
        self.assertEqual(self.state.name, "California")

    def test_state_to_dict(self):
        """Test State to_dict method includes all attributes"""
        self.state.name = "California"
        obj_dict = self.state.to_dict()
        
        self.assertEqual(obj_dict["__class__"], "State")
        self.assertEqual(obj_dict["name"], "California")

    def test_state_from_dict(self):
        """Test State creation from dictionary"""
        test_dict = {
            "id": "test-id",
            "created_at": "2023-01-01T12:00:00.000000",
            "updated_at": "2023-01-01T12:00:00.000000",
            "name": "California"
        }
        
        state = State(**test_dict)
        
        self.assertEqual(state.id, "test-id")
        self.assertEqual(state.name, "California")

    def test_state_storage_integration(self):
        """Test State integrates with storage"""
        key = f"State.{self.state.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key], self.state)


if __name__ == '__main__':
    unittest.main()
