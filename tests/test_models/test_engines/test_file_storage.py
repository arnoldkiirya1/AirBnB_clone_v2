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

    def test_new_instance_in_all(self):
        """Test if a newly created instance is present in all()"""
        user = User()
        self.storage.new(user)
        all_objects = self.storage.all()
        self.assertIn('User.' + user.id, all_objects)

    def test_new_instance_in_file(self):
        """Test if a newly created instance is saved to the file"""
        user = User()
        self.storage.new(user)
        self.storage.save()
        self.storage.reload()
        all_objects = self.storage.all()
        self.assertIn('User.' + user.id, all_objects)

    def test_delete_instance(self):
        """Test deleting an instance"""
        user = User()
        self.storage.new(user)
        self.storage.save()
        self.storage.delete(user)
        all_objects = self.storage.all()
        self.assertNotIn('User.' + user.id, all_objects)

    def test_count_instances(self):
        """Test counting instances in the storage"""
        count_before = len(self.storage.all())
        user = User()
        self.storage.new(user)
        self.storage.save()
        count_after = len(self.storage.all())
        self.assertEqual(count_after, count_before + 1)

    def test_get_instance_by_id(self):
        """Test getting an instance by its ID"""
        user = User()
        self.storage.new(user)
        self.storage.save()
        retrieved_user = self.storage.get(User, user.id)
        self.assertEqual(user, retrieved_user)

    def test_get_instance_by_nonexistent_id(self):
        """Test getting a nonexistent instance by ID"""
        retrieved_user = self.storage.get(User, 'nonexistent_id')
        self.assertIsNone(retrieved_user)

    def test_count_class_instances(self):
        """Test counting instances of a specific class"""
        count_before = len(self.storage.all(User))
        user1 = User()
        user2 = User()
        self.storage.new(user1)
        self.storage.new(user2)
        self.storage.save()
        count_after = len(self.storage.all(User))
        self.assertEqual(count_after, count_before + 2)

    def test_reload_empty_file(self):
        """Test reloading when the file is empty"""
        self.storage.reload()
        all_objects = self.storage.all()
        self.assertEqual(len(all_objects), 0)

    def test_reload_with_saved_data(self):
        """Test reloading with previously saved data"""
        user = User()
        self.storage.new(user)
        self.storage.save()
        self.storage.reload()
        all_objects = self.storage.all()
        self.assertIn('User.' + user.id, all_objects)

    def test_delete_nonexistent_instance(self):
        """Test deleting a nonexistent instance"""
        user = User()
        self.storage.delete(user)
        all_objects = self.storage.all()
        self.assertNotIn('User.' + user.id, all_objects)

    def test_multiple_saves(self):
        """Test saving multiple times without changes"""
        initial_data = self.storage.all()
        self.storage.save()
        self.storage.save()
        self.storage.reload()
        reloaded_data = self.storage.all()
        self.assertEqual(initial_data, reloaded_data)

    def test_empty_get(self):
        """Test getting with no arguments"""
        all_objects = self.storage.all()
        self.assertIsNone(self.storage.get(None, None))

    def test_get_nonexistent_instance(self):
        """Test getting a nonexistent instance"""
        retrieved_user = self.storage.get(User, 'nonexistent_id')
        self.assertIsNone(retrieved_user)

    def test_count_empty_class_instances(self):
        """Test counting instances of a specific class with empty storage"""
        count = len(self.storage.all(User))
        self.assertEqual(count, 0)

    def test_delete_instance_then_reload(self):
        """Test deleting an instance and then reloading"""
        user = User()
        self.storage.new(user)
        self.storage.save()
        self.storage.delete(user)
        self.storage.reload()
        all_objects = self.storage.all()
        self.assertNotIn('User.' + user.id, all_objects)

    def test_count_instances_multiple_classes(self):
        """Test counting instances of multiple classes"""
        count_user_before = len(self.storage.all(User))
        count_state_before = len(self.storage.all(State))
        user = User()
        state = State()
        self.storage.new(user)
        self.storage.new(state)
        self.storage.save()
        count_user_after = len(self.storage.all(User))
        count_state_after = len(self.storage.all(State))
        self.assertEqual(count_user_after, count_user_before + 1)
        self.assertEqual(count_state_after, count_state_before + 1)

    def test_delete_instance_and_reload(self):
        """Test deleting an instance and reloading"""
        user = User()
        self.storage.new(user)
        self.storage.save()
        self.storage.delete(user)
        self.storage.reload()
        all_objects = self.storage.all()
        self.assertNotIn('User.' + user.id, all_objects)

    def test_count_instances_multiple_classes(self):
        """Test counting instances of multiple classes"""
        count_user_before = len(self.storage.all(User))
        count_state_before = len(self.storage.all(State))
        user = User()
        state = State()
        self.storage.new(user)
        self.storage.new(state)
        self.storage.save()
        count_user_after = len(self.storage.all(User))
        count_state_after = len(self.storage.all(State))
        self.assertEqual(count_user_after, count_user_before + 1)
        self.assertEqual(count_state_after, count_state_before + 1)

    def test_all_with_specific_class(self):
        """Test retrieving instances of a specific class"""
        user1 = User()
        user2 = User()
        state = State()
        self.storage.new(user1)
        self.storage.new(user2)
        self.storage.new(state)
        self.storage.save()
        all_users = self.storage.all(User)
        self.assertIn('User.' + user1.id, all_users)
        self.assertIn('User.' + user2.id, all_users)
        self.assertNotIn('State.' + state.id, all_users)

    def test_get_instance(self):
        """Test retrieving an instance by class name and ID"""
        user = User()
        self.storage.new(user)
        self.storage.save()
        retrieved_user = self.storage.get(User, user.id)
        self.assertEqual(retrieved_user, user)

    def test_get_nonexistent_instance(self):
        """Test retrieving a nonexistent instance"""
        retrieved_user = self.storage.get(User, 'nonexistent_id')
        self.assertIsNone(retrieved_user)


if __name__ == '__main__':
    unittest.main()
