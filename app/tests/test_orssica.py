import unittest
from app.main.orssica import Orssica

class TestOrssica(unittest.TestCase):

    def test_get_exchange_rate(self):
        self.assertTrue(Orssica.get_exchange_rate())


if __name__ == "__main__":
    unittest.main()