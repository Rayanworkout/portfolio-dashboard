import dotenv
import os
import requests
import sys

from datetime import datetime

# Adding the parent directory to the path so that we can import the database module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time

from database import DbWorker

dotenv.load_dotenv()


class Portfolio:

    cache = {}

    def __init__(
        self, name: str = "main", db_name: str = "portfolio/portfolio.sqlite3"
    ) -> None:
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

        # return 1000  # testing purposes

        crypto = crypto.lower()

        if (
            crypto in Portfolio.cache
            and time.time() - Portfolio.cache[crypto]["timestamp"] < 3600
        ):  # Cache expires after 1 hour
            return Portfolio.cache[crypto]["price"]

        CGECKO_API_KEY = os.getenv("CGECKO_API_KEY")

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd&precision=2"

        try:
            response = requests.get(
                url, headers={"X-CoinGecko-API-Key": CGECKO_API_KEY}
            ).json()

            if response == {}:
                return None

            price = response[crypto]["usd"]

            Portfolio.cache[crypto] = {"price": price, "timestamp": time.time()}

            return price

        except KeyError:
            print("Rate limit exceeded. Waiting for a few seconds..")

    @classmethod
    def get_all_cgecko_tokens(cls) -> list:
        """
        Get all the tokens available on CoinGecko.

        """

        url = "https://api.coingecko.com/api/v3/coins/list"
        try:
            response = requests.get(url).json()
            print(f"Fetched {len(response)} tokens from CoinGecko ...")
            return [token["id"] for token in response]
        except Exception as e:
            print(f"Error: {e}")
            return []

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

    def get_token_transactions(self, token: str) -> list:
        """
        Get all the transactions of a specified token.

        """

        token_tx = self.df[self.df["token"] == token]

        transactions_dict = token_tx.to_dict("records")

        transactions_dict_with_formatted_date = []

        # For each transaction , I reformat fate to dd/mm/yyyy
        for transaction in transactions_dict:
            transaction["date"] = datetime.strptime(
                transaction["date"], "%Y-%m-%d %H:%M:%S"
            ).strftime("%d/%m/%Y")

            transactions_dict_with_formatted_date.append(transaction)

        return transactions_dict_with_formatted_date

    def get_profit(
        self,
        token: str = None,
        include_fees: bool = True,
        percentage: bool = False,
        total_value: int = 0,
    ) -> float:
        """
        Get the current profit of all transactions or a token.

        """

        if token is None:
            total_cost = self.df["cost"].sum()

            if include_fees:
                total_cost += self.df["fees"].sum()

            total_profit = total_value - total_cost

            if percentage is True and total_cost == 0:
                return 0

            return (
                total_profit if percentage is False else total_profit / total_cost * 100
            )

        token_transactions = self.df[self.df["token"] == token]

        token_cost_sum = token_transactions["cost"].sum()

        if include_fees:
            token_cost_sum += token_transactions["fees"].sum()

        token_profit = token_cost_sum - self.get_token_value(token)

        if percentage is True and token_cost_sum == 0:
            return 0

        return (
            token_profit if percentage is False else token_profit / token_cost_sum * 100
        )

    def get_all_tokens_with_their_value_and_holdings(self) -> list:
        """
        Get a list of all the tokens as well as the holdings
        and the value for each.

        """

        # I group by tokens and I compute the sum of each column
        data = self.df.groupby("token").sum()

        tokens = data.index

        if len(tokens) == 0:
            return []

        # Then I add some more columns if token list is not empty
        for token in tokens:
            data.loc[token, "value"] = self.get_token_value(token)
            data.loc[token, "profit"] = self.get_profit(token)
            data.loc[token, "profit_percentage"] = self.get_profit(
                token, percentage=True
            )

        # I select the columns I want to convert to a dictionary
        selected_columns = data[
            ["qty", "value", "fees", "cost", "profit", "profit_percentage"]
        ]

        # I reset the index (otherwise 'token' does not appear)
        # and convert the DataFrame to a list of dictionaries
        return selected_columns.reset_index().to_dict("records")

    def get_stablecoins_value(self) -> int:
        """
        Get the total value of all the stablecoins in the database.

        """
        # I group by tokens and I compute the sum of each column
        data = self.df.groupby("token").sum()

        # Filter the DataFrame to keep only the stablecoins
        data = data[data.index.isin(["usd-coin", "tether"])]

        return data.sum()["qty"]

    def get_value_history(self) -> dict:
        """
        Get the history of the portfolio value.

        """

        df = self.db.to_dataframe("portfolio_value")

        # I group by date and I compute the sum of each column
        data = df.groupby("date").sum()

        # I delete 'id' column
        data.drop("id", axis=1, inplace=True)

        dict_data = data.to_dict()

        return dict_data

    def __repr__(self) -> str:
        return f"Portfolio(name={self.name})"


if __name__ == "__main__":
    p = Portfolio()
    print(p.get_total_value())
