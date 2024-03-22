import sqlite3
import pandas as pd


class DbWorker:
    def __init__(self, db_name="portfolio.sqlite3"):
        self.__conn = sqlite3.connect(db_name)
        self.__cursor = self.__conn.cursor()

        self.__cursor.execute(
            "CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, qty REAL, cost REAL, fees REAL, token TEXT, date date DEFAULT CURRENT_TIMESTAMP)"
        )

        self.__cursor.execute(
            "CREATE TABLE IF NOT EXISTS portfolio_value (id INTEGER PRIMARY KEY, value REAL, date date DEFAULT CURRENT_TIMESTAMP)"
        )

    ################### CRUD OPERATIONS ###################
    def add_transaction(self, transaction: dict) -> None:
        """
        Add a new transaction to the database.

        """

        qty, cost, fees, token = (
            transaction["qty"],
            transaction["cost"],
            transaction["fees"],
            transaction["token"],
        )

        with self.__conn:
            self.__cursor.execute(
                "INSERT INTO transactions (qty, cost, fees, token) VALUES (?, ?, ?, ?)",
                (qty, cost, fees, token),
            )

            return self.__cursor.lastrowid

    def delete_transaction(self, id):
        """
        Deletes a transaction from the database.

        """
        with self.__conn:
            self.__cursor.execute(f"DELETE FROM transactions WHERE id = {id}")

    def insert_current_value_for_chart(self, value: float) -> None:
        """
        Insert the current value of the portfolio to the database.

        """
        with self.__conn:
            self.__cursor.execute(
                "INSERT INTO portfolio_value (value) VALUES (?)", (value,)
            )

    ################### GETTERS ###################
    def to_dataframe(self, table_name: str = "transactions"):
        """
        Convert transactions table to a pandas DataFrame.

        Parameters:
        - table_name (str): The name of the table to convert.

        Returns:
        - pd.DataFrame: A DataFrame containing the data from the specified table.
        """
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, self.__conn)
        return df

    ################### DESTRUCTORS ###################
    def __del__(self):
        self.__conn.close()

    def delete_all_transactions(self):
        with self.__conn:
            self.__cursor.execute("DELETE FROM transactions")

    ################### FAKER ###################
    def add_fake_transactions(self):
        transactions = [
            {"qty": 1, "cost": 100, "fees": 50, "token": "ethereum"},
            {"qty": 2, "cost": 200, "fees": 0, "token": "ethereum"},
            {"qty": 3, "cost": 300, "fees": 0, "token": "ethereum"},
            {"qty": 4, "cost": 400, "fees": 0, "token": "ethereum"},
            {"qty": 0.055, "cost": 500, "fees": 0, "token": "bitcoin"},
            {"qty": 6, "cost": 600, "fees": 40, "token": "ethereum"},
            {"qty": 7, "cost": 700, "fees": 0, "token": "ethereum"},
            {"qty": 0.05, "cost": 800, "fees": 0, "token": "bitcoin"},
            {"qty": 9, "cost": 900, "fees": 10, "token": "ethereum"},
            {"qty": 10, "cost": 1000, "fees": 0, "token": "ethereum"},
        ]

        for transaction in transactions:
            self.add_transaction(transaction)


if __name__ == "__main__":
    db = DbWorker("fake_data.sqlite3")
    db.add_fake_transactions()
