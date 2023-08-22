#!/usr/bin/python3
# tests db

import unittest
import MySQLdb
from models.state import State
from models.engine.db_storage import DBStorage


class TestDBStorageWithMySQL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Connect to the test MySQL database
        cls.db = MySQLdb.connect(
                host="localhost",
                user="testuser",
                passwd="testpass",
                db="testdb"
                )
        cls.cursor = cls.db.cursor()

        # Set up DBStorage and create tables
        cls.storage = DBStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        # Close the database connection
        cls.db.close()

    def test_add_state_to_db(self):
        # Get initial count of records in the states table
        initial_count = self._get_states_count()

        # Create a new State object
        new_state = State(name="California")

        # Add the State object to the session and commit to the database
        self.storage.new(new_state)
        self.storage.save()

        # Get count of records in the states table after adding the new State
        final_count = self._get_states_count()

        # Check if the count increased by 1 after adding the new State
        self.assertEqual(final_count, initial_count + 1)

    def _get_states_count(self):
        # Execute SQL query to get the count of records in the states table
        self.cursor.execute("SELECT COUNT(*) FROM states")
        count = self.cursor.fetchone()[0]
        return count


if __name__ == "__main__":
    unittest.main()
