#!/usr/bin/python3
# test module for class FileStorage
import unittest
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        """sets up an instance of FileStorage for the test"""
        self.storage = FileStorage()
        self.storage._FileStorage__objects = {}

    def tearDown(self):
        """cleans up after a test"""
        self.storage._FileStorage__objects = {}
        if os.path.exists(self.storage._FileStorage__file_path):
            os.remove(self.storage._FileStorage__file_path)

    """def test_reload_file_not_there(self):
        #tests the reload method in case file doesnt exits
        self.storage.reload()
        #since reload saves to __objects
        #a non existent file leads to an empty __objects
        self.assertEqual(len(self.storage.all()), 0)"""

    def test_save_and_reload(self):
        """test the save and reload methods"""
        # create instances of various classes

        user = User()
        place = Place()
        city = City()
        amenity = Amenity()
        review = Review()
        state = State()

        # Add instances to storage
        self.storage.new(user)
        self.storage.new(place)
        self.storage.new(city)
        self.storage.new(amenity)
        self.storage.new(review)
        self.storage.new(state)

        # Save instances to file
        self.storage.save()

        # Reload instances from file
        self.storage.reload()

        # check if reloaded instances are present in __objects
        self.assertIn('User.' + user.id, self.storage.all())
        self.assertIn('Place.' + place.id, self.storage.all())
        self.assertIn('City.' + city.id, self.storage.all())
        self.assertIn('Amenity.' + amenity.id, self.storage.all())
        self.assertIn('Review.' + review.id, self.storage.all())
        self.assertIn('State.' + state.id, self.storage.all())

    def test_save_file_exists(self):
        """test if file from save method is exists"""
        # create instance
        city = City()

        # add to storage
        self.storage.new(city)

        # save to file
        self.storage.save()

        # check if file exists
        self.assertTrue(os.path.exists(self.storage._FileStorage__file_path))


if __name__ == '__main__':
    unittest.main()
