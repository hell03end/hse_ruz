import unittest
from ruz import RUZ


class TestRUZ(unittest.TestCase):
    def setUp(self):
        self.api = RUZ()

    def test_v(self):
        self.assertEqual(self.api.v, 2)

    def test_get(self):
        self.assertTrue(self.api.get("chairs"))


if __name__ == "__main__":
    unittest.main()
