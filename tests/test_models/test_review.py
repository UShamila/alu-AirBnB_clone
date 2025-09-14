#!/usr/bin/python3
"""
Unit tests for Review class
"""
import unittest
import os
from models.review import Review
from models import storage


class TestReview(unittest.TestCase):
    """Test cases for Review class"""

    def setUp(self):
        """Set up test fixtures"""
        # Clear storage before each test
        storage.all().clear()
        self.review = Review()

    def tearDown(self):
        """Clean up after each test"""
        # Clear storage after each test
        storage.all().clear()
        # Remove file.json if it exists
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_review_inheritance(self):
        """Test that Review inherits from BaseModel"""
        from models.base_model import BaseModel
        self.assertIsInstance(self.review, BaseModel)

    def test_review_attributes(self):
        """Test Review class attributes"""
        self.assertEqual(self.review.place_id, "")
        self.assertEqual(self.review.user_id, "")
        self.assertEqual(self.review.text, "")

    def test_review_attributes_assignment(self):
        """Test Review attributes can be assigned"""
        self.review.place_id = "place-123"
        self.review.user_id = "user-123"
        self.review.text = "Great place to stay!"
        self.assertEqual(self.review.place_id, "place-123")
        self.assertEqual(self.review.user_id, "user-123")
        self.assertEqual(self.review.text, "Great place to stay!")

    def test_review_to_dict(self):
        """Test Review to_dict method includes all attributes"""
        self.review.place_id = "place-123"
        self.review.user_id = "user-123"
        self.review.text = "Great place to stay!"
        obj_dict = self.review.to_dict()
        
        self.assertEqual(obj_dict["__class__"], "Review")
        self.assertEqual(obj_dict["place_id"], "place-123")
        self.assertEqual(obj_dict["user_id"], "user-123")
        self.assertEqual(obj_dict["text"], "Great place to stay!")

    def test_review_from_dict(self):
        """Test Review creation from dictionary"""
        test_dict = {
            "id": "test-id",
            "created_at": "2023-01-01T12:00:00.000000",
            "updated_at": "2023-01-01T12:00:00.000000",
            "place_id": "place-123",
            "user_id": "user-123",
            "text": "Great place to stay!"
        }
        
        review = Review(**test_dict)
        
        self.assertEqual(review.id, "test-id")
        self.assertEqual(review.place_id, "place-123")
        self.assertEqual(review.user_id, "user-123")
        self.assertEqual(review.text, "Great place to stay!")

    def test_review_storage_integration(self):
        """Test Review integrates with storage"""
        key = f"Review.{self.review.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key], self.review)


if __name__ == '__main__':
    unittest.main()
