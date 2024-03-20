
import unittest

from portfolio import Portfolio


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.pf = Portfolio("test", db_name="portfolio/test.sqlite3")
    
    def tearDown(self) -> None:
        self.pf.db.delete_all_transactions()

    def test_get_total_value_empty(self):
        self.assertEqual(self.pf.get_total_value(), 0)

    def test_get_profit_empty(self):
        self.assertEqual(self.pf.get_profit(), 0)

    def test_get_token_value_empty(self):
        self.assertEqual(self.pf.get_token_value("BTC"), 0)

    def test_get_total_value(self):
        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.pf.db.delete_all_transactions()

        self.pf.db.add_transaction(tx)
        self.assertEqual(self.pf.get_total_value(), 500)


if __name__ == "__main__":
    unittest.main()
