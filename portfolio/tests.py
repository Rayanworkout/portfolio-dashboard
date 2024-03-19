import unittest


import unittest

from portfolio import Portfolio
from database.worker import DbWorker


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.pf = Portfolio("test")
        self.db = DbWorker("test.sqlite3")

    def tearDown(self) -> None:
        pass

    def test_get_total_value(self):
        self.assertEqual(self.pf.get_total_value(testing=True), 0)
    
    def test_get_token_value(self):
        self.assertEqual(self.pf.get_token_value("BTC", testing=True), 0)


if __name__ == "__main__":
    unittest.main()
