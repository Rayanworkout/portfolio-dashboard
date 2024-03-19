import os

import dotenv
import requests

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import DbWorker

transactions = [
    {"qty": 0.4198, "cost": 1500, "fees": 10, "token": "ETH", "date": "2021-10-10"},
    {"qty": 0.0225, "cost": 0, "fees": 0, "token": "ETH", "date": "2021-10-10"},
]

dotenv.load_dotenv()


class Portfolio:

    def __init__(self, name: str = "main") -> None:
        self.name = name

        self.db = DbWorker()

    @staticmethod
    def __get_price(crypto: str) -> float:
        """
        Get the price of a cryptocurrency in USD using the CoinGecko API.

        You need to use a free API key that must be placed in the .env file.
        https://www.coingecko.com/en/api

        """

        CGECKO_API_KEY = os.getenv("CGECKO_API_KEY")

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd&precision=2"

        response = requests.get(
            url, headers={"X-CoinGecko-API-Key": CGECKO_API_KEY}
        ).json()

        return response[crypto]["usd"]

    def get_total_value(self) -> float:
        """
        Get the total value of all transactions in the database.

        """
        total_value = 0

        for transaction in self.db.get_all_transactions():
            qty, _, _, token = transaction

            price = self.__get_price(token)

            total_value += qty * price

        return total_value

    def get_token_value(self, token: str) -> float:
        """
        Get the total value of a specified token.

        """
        token_transactions = self.db.get_token_transactions(token)
        price = self.__get_price(token)

        total_value = 0

        for transaction in token_transactions:
            qty, _, _, _ = transaction

            total_value += qty * price

    def get_profit(self, token: str = None) -> float:
        """
        Get the current profit of all transactions in the database.

        """
        if token is None:
            return self.get_total_value() - self.db.get_total_cost()

        return self.get_token_value(token) - self.db.get_token_cost(token)

    def get_profit_percentage(self, token: str = None) -> float:
        """
        Get the current profit percentage of all transactions in the database.

        """
        if token is None:
            return (self.get_profit() / self.db.get_total_cost()) * 100

        return (self.get_profit(token) / self.db.get_token_cost(token)) * 100

    def __repr__(self) -> str:
        return f"Portfolio(name={self.name})"


pf = Portfolio()

print(pf.get_total_value())
