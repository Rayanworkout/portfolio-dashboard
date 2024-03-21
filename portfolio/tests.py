import unittest

from portfolio import Portfolio


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        # Each pf has a database instance linked
        self.pf = Portfolio("test", db_name="portfolio/test.sqlite3")

    def tearDown(self) -> None:
        self.pf.db.delete_all_transactions()
        pass

    def test_get_total_value_empty(self):
        self.assertEqual(self.pf.get_total_value(), 0)

    def test_get_profit_empty(self):
        self.assertEqual(self.pf.get_profit(), 0)

    def test_get_token_value_empty(self):
        self.assertEqual(self.pf.get_token_value("BTC"), 0)
    
    def test_get_profit_percentage_empty(self):
        self.assertEqual(self.pf.get_profit(percentage=True), 0)



if __name__ == "__main__":
    unittest.main()
