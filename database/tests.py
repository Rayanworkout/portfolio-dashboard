import unittest

from database.crypto_worker import DbWorker

class TestDbWorker(unittest.TestCase):
    def setUp(self):
        self.db = DbWorker("database/tests.sqlite3")

    def tearDown(self) -> None:
        self.db.delete_all_transactions()
        del self.db

    def test_add_transaction(self):
        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.db.add_transaction(tx)

        all_tx = self.db.get_all_transactions()

        self.assertIsNotNone(all_tx)
        self.assertEqual(len(all_tx), 1)

    def test_delete_transaction(self):
        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.db.add_transaction(tx)
        self.db.delete_transaction(1)

        all_tx = self.db.get_all_transactions()

        self.assertEqual(len(all_tx), 0)

    def test_get_token_transactions(self):
        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.db.add_transaction(tx)

        token_tx = self.db.get_token_transactions("ethereum")

        self.assertIsNotNone(token_tx)
        self.assertEqual(len(token_tx), 1)

    def test_total_qty(self):
        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.db.add_transaction(tx)

        total_qty = self.db.get_total_qty("ethereum")

        self.assertEqual(total_qty, 0.5)

    def test_total_cost(self):

        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.db.add_transaction(tx)

        total_cost = self.db.get_total_cost()

        # with fees
        self.assertEqual(total_cost, 510)

        # without fees
        total_cost_no_fees = self.db.get_total_cost(include_fees=False)

        self.assertEqual(total_cost_no_fees, 500)

    def test_get_token_cost(self):
        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.db.add_transaction(tx)

        token_cost = self.db.get_token_cost("ethereum")

        # with fees
        self.assertEqual(token_cost, 510)

        # without fees
        token_cost_no_fees = self.db.get_token_cost("ethereum", include_fees=False)

        self.assertEqual(token_cost_no_fees, 500)

    def test_get_avg_buy_price(self):

        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.db.add_transaction(tx)

        avg_buy_price = self.db.get_avg_buy_price("ethereum")

        self.assertEqual(avg_buy_price, 1020)

    def test_get_avg_buy_price_no_transactions(self):
        avg_buy_price = self.db.get_avg_buy_price("ethereum")

        self.assertEqual(avg_buy_price, 0)


if __name__ == "__main__":
    unittest.main()
