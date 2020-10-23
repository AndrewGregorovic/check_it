import unittest

from src.main import add


class DummyTest(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(2,3), 5)
