import sqlite3


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

    def delete_transaction(self, id):
        """
        Deletes a transaction from the database.

        """
        with self.__conn:
            self.__cursor.execute(f"DELETE FROM transactions WHERE id = {id}")

    ################### GETTERS ###################

    def get_all_transactions(self):
        """
        Get all transactions from the database.

        """
        with self.__conn:
            self.__cursor.execute("SELECT * FROM transactions")
            return self.__cursor.fetchall()

    def get_token_transactions(self, token: str):
        """
        Get all transactions from a specified token.

        """
        with self.__conn:
            self.__cursor.execute(f"SELECT * FROM transactions WHERE token = '{token}'")
            return self.__cursor.fetchall()

    def get_total_cost(self, include_fees=True) -> float:
        """
        Get the total cost of all transactions in the database, including fees or not.

        """

        if include_fees is True:
            self.__cursor.execute("SELECT SUM(cost + fees) FROM transactions")
        else:
            self.__cursor.execute("SELECT SUM(cost) FROM transactions")

        result = self.__cursor.fetchone()

        if result is None:
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

    def get_total_qty(self, token: str) -> float:
        """
        Get the total owned quantity of a specified token.

        """
        self.__cursor.execute(
            f"SELECT SUM(qty) FROM transactions WHERE token = '{token}'"
        )

        result = self.__cursor.fetchone()

        if result[0] is None:
            return 0
        else:
            total_qty = result[0]
            return total_qty

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
