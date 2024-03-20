import unittest

from portfolio import Portfolio


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        # Each pf has a database instance linked
        self.pf = Portfolio("test", db_name="portfolio/test.sqlite3")

    def tearDown(self) -> None:
        self.pf.db.delete_all_transactions()

    def test_get_total_value_empty(self):
        self.assertEqual(self.pf.get_total_value(), 0)

    def test_get_profit_empty(self):
        self.assertEqual(self.pf.get_profit(), 0)

    def test_get_token_value_empty(self):
        self.assertEqual(self.pf.get_token_value("BTC"), 0)
    
    def test_get_profit_percentage_empty(self):
        self.assertEqual(self.pf.get_profit_percentage(), 0)

    def test_get_total_value(self):
        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.pf.db.add_transaction(tx)
        self.assertEqual(self.pf.get_total_value(), 500)
 
    def test_get_total_profit(self):
        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.pf.db.add_transaction(tx)

        self.assertEqual(self.pf.get_profit(), -10) # 10$ fees

        # Without fees
        self.assertEqual(self.pf.get_profit(include_fees = False), 0)

    def test_get_token_profit(self):
        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.pf.db.add_transaction(tx)

        self.assertEqual(self.pf.get_token_value("ethereum"), 500)

        self.assertEqual(self.pf.get_profit("ethereum"), -10) # 10$ fees

    def get_token_profit_percentage(self):
        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.pf.db.add_transaction(tx)

        self.assertEqual(self.pf.get_profit_percentage("ethereum"), -2) # 10$ fees = 2%

        # Without fees
        self.assertEqual(self.pf.get_profit_percentage("ethereum", include_fees = False), 0)



if __name__ == "__main__":
    unittest.main()
