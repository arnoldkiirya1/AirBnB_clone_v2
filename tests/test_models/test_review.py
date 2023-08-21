#!/usr/bin/python3
# Tests for class Review
import unittest
from models.review import Review


class TestReview(unittest.TestCase):
    def test_attributes(self):
        city = Review()
        self.assertTrue(hasattr(city, 'id'))
        self.assertTrue(hasattr(city, 'created_at'))
        self.assertTrue(hasattr(city, 'updated_at'))
        self.assertTrue(hasattr(city, 'place_id'))
        self.assertTrue(hasattr(city, 'user_id'))
        self.assertTrue(hasattr(city, 'text'))

    def test_name_default_value(self):
        place = Review()
        self.assertEqual(place.place_id, "")
        self.assertEqual(place.user_id, "")
        self.assertEqual(place.text, "")

    def test_attribute_assignment(self):
        place = Review()
        place.place_id = "123"
        place.user_id = "456"
        place.text = "Cozy Cabin"
        self.assertEqual(place.place_id, "123")
        self.assertEqual(place.user_id, "456")
        self.assertEqual(place.text, "Cozy Cabin")


if __name__ == '__main__':
    unittest.main()
