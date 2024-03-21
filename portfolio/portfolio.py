import os
import dotenv
import requests

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import DbWorker

dotenv.load_dotenv()


class Portfolio:

    def __init__(self, name: str = "main", db_name: str = "portfolio.sqlite3") -> None:
        self.name = name
        self.db = DbWorker(db_name=db_name)

        self.df = self.db.to_dataframe()

    @staticmethod
    def __get_price(crypto: str) -> float:
        """
        Get the price of a cryptocurrency in USD using the CoinGecko API.

        You need to use a free API key that must be placed in the .env file.
        https://www.coingecko.com/en/api

        """

        return 1000  # testing purposes

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
        # Grouping tokens
        token_groups = self.df.groupby("token")

        # Getting the total value of each token
        total_qty = token_groups["qty"].sum()

        # Getting the price of each token
        token_prices = total_qty.index.map(self.__get_price)

        # Applying the price to the total quantity
        total_value = total_qty * token_prices

        return total_value.sum()

    def get_token_value(self, token: str) -> float:
        """
        Get the total value of a specified token.

        """

        price = self.__get_price(token)

        token_tx = self.df[self.df["token"] == token]

        return token_tx["qty"].sum() * price

    def get_profit(self, token: str = None, include_fees: bool = True) -> float:
        """
        Get the current profit of all transactions or a token.

        """

        if token is None:
            total_cost = self.df["cost"].sum()

            if include_fees:
                total_cost += self.df["fees"].sum()

            return self.get_total_value() - total_cost

        token_transactions = self.df[self.df["token"] == token]

        token_cost_sum = token_transactions["cost"].sum()

        if include_fees:
            token_cost_sum += token_transactions["fees"].sum()
        
        return token_cost_sum - self.get_token_value(token)
    
    def get_profit_percentage(self, token: str = None) -> float:
        """
        Get the current profit percentage of all transactions or a token.

        """
        if token is None:
            total_cost = self.df["cost"].sum()

            return self.get_profit() / total_cost * 100
        

        

    def get_all_tokens_with_their_value_and_holdings(self) -> list:
        """
        Get a list of all the tokens as well as the holdings
        and the value for each.

        """
        all_tokens = self.db.get_unique_tokens()

        token_values = []

        for token in all_tokens:
            token_values.append(
                {
                    "token": token,
                    "value": self.get_token_value(token),
                    "holdings": self.db.get_token_qty(token),
                }
            )

        return token_values

    def __repr__(self) -> str:
        return f"Portfolio(name={self.name})"


pf = Portfolio(db_name="fake_data.sqlite3")

print(pf.get_profit_percentage())
