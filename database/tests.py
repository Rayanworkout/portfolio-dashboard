import unittest

from crypto_worker import DbWorker


class TestDbWorker(unittest.TestCase):
    def setUp(self):
        self.db = DbWorker("database/tests.sqlite3")

    def tearDown(self) -> None:
        self.db.delete_all_transactions()
        del self.db

    def test_to_dataframe(self):
        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.db.add_transaction(tx)
        df = self.db.to_dataframe()

        self.assertIsNotNone(df)

    def test_add_transaction(self):
        tx = {
            "cost": 500,
            "fees": 10,
            "qty": 0.5,
            "token": "ethereum",
        }

        self.db.add_transaction(tx)

        all_tx = self.db.to_dataframe()

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

        all_tx = self.db.to_dataframe()

        self.assertEqual(len(all_tx), 0)


if __name__ == "__main__":
    unittest.main()
