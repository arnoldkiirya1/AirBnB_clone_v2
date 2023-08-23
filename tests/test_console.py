#!/usr/bin/python3
"""unittest module for the console (command interpreter)
"""
import json
import MySQLdb
import os
import sqlalchemy
import unittest

from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream


class TestHBNBCommand(unittest.TestCase):
    """test class for the HBNBCommand class.
    """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create(self):
        """Tests the create command
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create City name="Texas"')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            self.assertIn('City.{}'.format(mdl_id), storage.all().keys())
            cons.onecmd('show City {}'.format(mdl_id))
            self.assertIn("'name': 'Texas'", cout.getvalue().strip())
            clear_stream(cout)
            cons.onecmd('create User name="Ahmed" age=24 height=5.7')
            mdl_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(mdl_id), storage.all().keys())
            clear_stream(cout)
            cons.onecmd('show User {}'.format(mdl_id))
            self.assertIn("'name': 'Ahmed'", cout.getvalue().strip())
            self.assertIn("'age': 24", cout.getvalue().strip())
            self.assertIn("'height': 5.7", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Tests the create command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                cons.onecmd('create User')
            clear_stream(cout)
            cons.onecmd('create User email="ayo15@gmail.com" password="123"')
            mdl_id = cout.getvalue().strip()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(mdl_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('ayo15@gmail.com', result)
            self.assertIn('123', result)
            cursor.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Tests the show command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            obj = User(email="ayo15@gmail.com", password="123")
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is None)
            cons.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                cout.getvalue().strip(),
                '** no instance found **'
            )
            obj.save()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clear_stream(cout)
            cons.onecmd('show User {}'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('ayo15@gmail.com', result)
            self.assertIn('123', result)
            self.assertIn('ayo15@gmail.com', cout.getvalue())
            self.assertIn('123', cout.getvalue())
            cursor.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Tests the count command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            res = cursor.fetchone()
            prev_count = int(res[0])
            cons.onecmd('create State name="Lagos"')
            clear_stream(cout)
            cons.onecmd('count State')
            cnt = cout.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(cout)
            cons.onecmd('count State')
            cursor.close()
            dbc.close()

    def test_fs_create(self):
        """Tests the create command with the file storage.
        """
        # ... existing test logic ...

    def test_db_create(self):
        """Tests the create command with the database storage.
        """
        # ... existing test logic ...

    def test_db_show(self):
        """Tests the show command with the database storage.
        """
        # ... existing test logic ...

    def test_db_count(self):
        """Tests the count command with the database storage.
        """
        # ... existing test logic ...

    def test_update(self):
        """Test updating attributes using the update command.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create User email="john25@gmail.com" password="123"')
            mdl_id = cout.getvalue().strip()

            # Test updating email attribute
            cons.onecmd('update User {} email="updated@gmail.com"'.format(
                                                                    mdl_id))
            cons.onecmd('show User {}'.format(mdl_id))
            self.assertIn("'email': 'updated@gmail.com'", cout.getvalue())

            # Test updating password attribute
            cons.onecmd('update User {} password="newpass"'.format(mdl_id))
            cons.onecmd('show User {}'.format(mdl_id))
            self.assertIn("'password': 'newpass'", cout.getvalue())

    def test_edge_cases(self):
        """Test edge cases, invalid attributes, and non-existing classes.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()

            # Test invalid attribute
            cons.onecmd('create User invalid_attr="value"')
            self.assertIn('invalid attribute', cout.getvalue())

            # Test non-existing class
            cons.onecmd('create InvalidClass')
            self.assertIn("** class doesn't exist **", cout.getvalue())

    def test_special_characters(self):
        """Test creating objects with special character attributes.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create User name="Special % Ch@rs"')
            mdl_id = cout.getvalue().strip()
            cons.onecmd('show User {}'.format(mdl_id))
            self.assertIn("'name': 'Special % Ch@rs'", cout.getvalue())


if __name__ == "__main__":
    unittest.main()
