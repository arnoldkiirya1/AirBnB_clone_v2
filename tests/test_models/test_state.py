#!/usr/bin/python3
# Tests for class State
import unittest
from models.state import State


class TestState(unittest.TestCase):
    def test_attributes(self):
        state = State()
        self.assertTrue(hasattr(state, 'id'))
        self.assertTrue(hasattr(state, 'created_at'))
        self.assertTrue(hasattr(state, 'updated_at'))
        self.assertTrue(hasattr(state, 'name'))

    def test_name_default_value(self):
        state = State()
        self.assertEqual(state.name, "")

    def test_name_assignment(self):
        state = State()
        state.name = "Wisdom"
        self.assertEqual(state.name, "Wisdom")


if __name__ == '__main__':
    unittest.main()
