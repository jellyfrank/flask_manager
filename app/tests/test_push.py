import unittest
from app.main.webserivce import PushProxy


class TestPush(unittest.TestCase):

    def test_push(self):
        pp = PushProxy()
        res = pp.test()
        self.assertEqual(res["success"], False)

        print(pp.push())


if __name__ == "__main__":
    unittest.main()
