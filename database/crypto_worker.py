import sqlite3
import pandas as pd


class DbWorker:
    def __init__(self, db_name="portfolio.sqlite3"):
        self.__conn = sqlite3.connect(db_name)
        self.__cursor = self.__conn.cursor()

        self.__cursor.execute(
            "CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, qty REAL, cost REAL, fees REAL, token TEXT, date date DEFAULT CURRENT_TIMESTAMP)"
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




    def get_unique_tokens(self) -> list:
        """
        Get all unique tokens in the database.

        """
        self.__cursor.execute("SELECT DISTINCT token FROM transactions")
        result = self.__cursor.fetchall()
        return [token[0] for token in result]

    def get_total_cost(self, include_fees=True) -> float:
        """
        Get the total cost of all transactions in the database, including fees or not.

        """

        if include_fees is True:
            self.__cursor.execute("SELECT SUM(cost + fees) FROM transactions")
        else:
            self.__cursor.execute("SELECT SUM(cost) FROM transactions")

        result = self.__cursor.fetchone()

        if result[0] is None:
            return 0
        else:
            total_cost = result[0]
            return round(total_cost, 2)

    def get_token_cost(self, token: str, include_fees=True) -> float:
        """
        Get the total cost of a specified token, including fees or not.

        """

        if include_fees is True:
            self.__cursor.execute(
                f"SELECT SUM(cost + fees) FROM transactions WHERE token = '{token}'"
            )
        else:
            self.__cursor.execute(
                f"SELECT SUM(cost) FROM transactions WHERE token = '{token}'"
            )

        result = self.__cursor.fetchone()

        if result[0] is None:
            return 0
        else:
            total_cost = result[0]
            return total_cost

    def get_avg_buy_price(self, token: str, include_fees=True) -> float:
        """
        Get the average buy price of a specified token.

        """
        token_cost, total_qty = self.get_token_cost(
            token, include_fees
        ), self.get_total_qty(token)

        if token_cost == 0 or total_qty == 0:
            return 0

        avg_price = token_cost / total_qty

        if avg_price is None:
            return 0

        return round(avg_price, 2)

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

        # Total qty: ETH = 42, BTC = 0.105
        # Total cost: ETH = 3300, BTC = 500
        # Total fees: ETH = 100, BTC = 0
        # eth price = 1000, btc price = 1000

        for transaction in transactions:
            self.add_transaction(transaction)


# if __name__ == "__main__":
#     db = DbWorker("fake_data.sqlite3")
#     db.add_fake_transactions()
