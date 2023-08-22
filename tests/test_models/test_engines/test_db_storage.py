#!/usr/bin/python3
# test for db_storage

import unittest
from models.engine.db_storage import DBStorage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class TestDBStorage(unittest.TestCase):
    def setUp(self):
        """Set up the test environment"""
        self.db = DBStorage()
        self.db.reload()
        self.session = self.db._DBStorage__session

    def tearDown(self):
        """Clean up after each test"""
        self.db.close()

    def test_create_and_retrieve_objects(self):
        """Test creating and retrieving objects from the database"""
        state = State(name="California")
        city = City(name="Los Angeles", state_id=state.id)
        user = User(email="test@example.com", password="password")
        
        # Add objects to session and save to the database
        self.session.add(state)
        self.session.add(city)
        self.session.add(user)
        self.session.commit()

        # Retrieve objects using all() method
        retrieved_state = self.db.all(State).get("State." + state.id)
        retrieved_city = self.db.all(City).get("City." + city.id)
        retrieved_user = self.db.all(User).get("User." + user.id)

        self.assertEqual(retrieved_state, state)
        self.assertEqual(retrieved_city, city)
        self.assertEqual(retrieved_user, user)

    def test_update_and_delete_objects(self):
        """Test updating and deleting objects from the database"""
        user = User(email="test@example.com", password="password")
        self.session.add(user)
        self.session.commit()

        # Update user object
        user.email = "updated@example.com"
        self.session.commit()

        # Retrieve updated user
        retrieved_user = self.db.all(User).get("User." + user.id)
        self.assertEqual(retrieved_user.email, "updated@example.com")

        # Delete user
        self.session.delete(user)
        self.session.commit()

        # Ensure user is not in the database
        retrieved_user = self.db.all(User).get("User." + user.id)
        self.assertIsNone(retrieved_user)

    def test_table_creation(self):
        """Test if tables are created properly"""
        # Ensure State table is created
        self.assertTrue(State.__tablename__ in self.db.__engine.table_names())

    def test_session_management(self):
        """Test if sessions are managed correctly"""
        user = User(email="test@example.com", password="password")
        self.session.add(user)
        self.session.commit()

        # Retrieve user in a new session
        new_session = self.db._DBStorage__session_factory()
        retrieved_user = new_session.query(User).filter_by(email="test@example.com").first()
        new_session.close()

        self.assertEqual(retrieved_user.email, "test@example.com")

if __name__ == '__main__':
    unittest.main()
