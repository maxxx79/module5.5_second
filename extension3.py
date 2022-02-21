import json
import requests
from bot_config import keys

class ConversionExeption(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConversionExeption(f'Невозможно перевести одинаковые валюты: "{base}".')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionExeption(f'Не удалось обработать валюту: "{quote}"')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionExeption(f'Не удалось обработать валюту "{base}"')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionExeption(f'Не удалось обработать количество: "{amount}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        total_price = float(total_base) * float(amount)

        return round(total_price, 3)
