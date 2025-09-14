# AirBnB Clone - Console

This repository contains the first part of the AirBnB clone project: a custom command-line interface (CLI) to manage AirBnB-like objects.

## Project Description

The AirBnB clone is a complete web application that replicates core functionality of the AirBnB platform. This first phase implements:
- A custom command interpreter to manipulate objects without a visual interface
- Storage engine to persist objects to a JSON file
- Basic object classes (User, State, City, Place, etc.)
- Unit tests to validate all functionality

## Command Interpreter Description

The console is a CLI program built with Python's `cmd` module that:
- Creates new objects (Users, Places, States, etc.)
- Retrieves objects from storage
- Performs operations on objects (show, update, destroy)
- Updates the JSON storage file

## Getting Started

### Prerequisites
- Python 3.8 or higher
- PEP 8 style compliance (pycodestyle)
