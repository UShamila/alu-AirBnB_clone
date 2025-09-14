#!/usr/bin/python3
"""
Models package initialization
"""
from models.engine.file_storage import FileStorage

# Create a unique FileStorage instance for the application
storage = FileStorage()

# Reload objects from storage
storage.reload()
