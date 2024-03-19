import unittest
import os

from worker import DbWorker


# add_transaction, delete_transaction, get_all_transactions, get_token_transactions, get_total_cost, get_token_cost, get_total_qty, get_avg_buy_price


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

        print(all_tx)

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


if __name__ == "__main__":
    unittest.main()
