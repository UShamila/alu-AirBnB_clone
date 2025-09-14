#!/usr/bin/python3
"""
Unit tests for User class
"""
import unittest
import os
from models.user import User
from models import storage


class TestUser(unittest.TestCase):
    """Test cases for User class"""

    def setUp(self):
        """Set up test fixtures"""
        # Clear storage before each test
        storage.all().clear()
        self.user = User()

    def tearDown(self):
        """Clean up after each test"""
        # Clear storage after each test
        storage.all().clear()
        # Remove file.json if it exists
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_user_inheritance(self):
        """Test that User inherits from BaseModel"""
        from models.base_model import BaseModel
        self.assertIsInstance(self.user, BaseModel)

    def test_user_attributes(self):
        """Test User class attributes"""
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    def test_user_attributes_assignment(self):
        """Test User attributes can be assigned"""
        self.user.email = "test@example.com"
        self.user.password = "password123"
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.password, "password123")
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")

    def test_user_to_dict(self):
        """Test User to_dict method includes all attributes"""
        self.user.email = "test@example.com"
        self.user.password = "password123"
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        
        obj_dict = self.user.to_dict()
        
        self.assertEqual(obj_dict["__class__"], "User")
        self.assertEqual(obj_dict["email"], "test@example.com")
        self.assertEqual(obj_dict["password"], "password123")
        self.assertEqual(obj_dict["first_name"], "John")
        self.assertEqual(obj_dict["last_name"], "Doe")

    def test_user_from_dict(self):
        """Test User creation from dictionary"""
        test_dict = {
            "id": "test-id",
            "created_at": "2023-01-01T12:00:00.000000",
            "updated_at": "2023-01-01T12:00:00.000000",
            "email": "test@example.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe"
        }
        
        user = User(**test_dict)
        
        self.assertEqual(user.id, "test-id")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "password123")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_user_str_representation(self):
        """Test User string representation"""
        self.user.email = "test@example.com"
        self.user.first_name = "John"
        
        expected = f"[User] ({self.user.id}) {self.user.__dict__}"
        self.assertEqual(str(self.user), expected)

    def test_user_storage_integration(self):
        """Test User integrates with storage"""
        key = f"User.{self.user.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key], self.user)


if __name__ == '__main__':
    unittest.main()
