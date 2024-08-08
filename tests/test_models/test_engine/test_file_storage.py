#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_existing_object(self):
        """Test Retrieve Existing Object"""
        user = BaseModel()
        user.name = "test user"
        models.storage.new(user)
        models.storage.save()

        retrieved_user = models.storage.get(BaseModel, user.id)

        self.assertIsNotNone(retrieved_user, "get() should return an object")
        self.assertEqual(retrieved_user.id, user.id, "The ID should match")
        self.assertEqual(retrieved_user.name, "test user", "name should match")

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_non_existing_object(self):
        """Test non existing object"""
        retrieved_user = models.storage.get(BaseModel, 'non_existent_id')

        self.assertIsNone(retrieved_user, "get() should return None")

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_invalid_id_format(self):
        """Test invalid ID format"""
        self.assertIsNone(models.storage.get(BaseModel, None), "get()")
        self.assertIsNone(models.storage.get(BaseModel, ''), "get()")
        self.assertIsNone(models.storage.get(BaseModel, '!!@@##'), "get()")

    @unittest .skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_invalid_class(self):
        """Test invalid Class format"""
        self.assertIsNone(models.storage.get('NonExistentclass', 'some_id'))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_all_objects(self):
        """Clear storage test"""
        FileStorage._FileStorage__objects.clear()

        user = User()
        place = Place()
        base_model = BaseModel()

        models.storage.new(user)
        models.storage.new(place)
        models.storage.new(base_model)
        models.storage.save()

        total_count = models.storage.count()

        self.assertEqual(total_count, 3, "count() return 3")

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_specific_class(self):
        """Clear storage"""
        FileStorage._FileStorage__objects.clear()

        user1 = User()
        user2 = User()
        place = Place()

        models.storage.new(user1)
        models.storage.new(user2)
        models.storage.new(place)
        models.storage.save()

        user_count = models.storage.count(User)
        self.assertEqual(user_count, 2, "count(User) should return 2")

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_empty_storage(self):
        """Clear storage"""
        FileStorage._FileStorage__objects.clear()

        total_count = models.storage.count()
        user_count = models.storage.count(User)

        self.assertEqual(total_count, 0, "count() should return 0")
        self.assertEqual(user_count, 0, "count(User) should return 0")

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_no_instances_of_class(self):
        """clear storage"""
        FileStorage._FileStorage__objects.clear()

        place = Place()
        base_model = BaseModel()

        models.storage.new(place)
        models.storage.new(base_model)
        models.storage.save()

        user_count = models.storage.count(User)

        self.assertEqual(user_count, 0, "co")
