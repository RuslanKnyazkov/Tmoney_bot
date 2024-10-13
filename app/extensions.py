from config import TIKERS
import requests
import json

class APIException(Exception):
    """
    Exception for class Currency.
    """
    pass


class Currency:
    """
    This class is designed to work with currency.
    """

    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> int | float:
        """
        This function requests the entered currencies from the user.
        :param base: Base currency.
        :param quote: Currency for conversion.
        :param amount: The amount of the base currency.
        :return: The result of the conversion multiplied by the number of coins.
        """

        if base == quote:
            raise APIException('Тикер валюты совпадает с конвертируемой валютой')

        if base not in TIKERS.keys():
            raise APIException(f'Тикер {base} не может быть конвертирован')

        if quote not in TIKERS.keys():
            raise APIException(f'Тикер {quote} не может быть конвертирован')

        if int(amount) <= 0:
            raise APIException('Пожалуйста введите положительное число больше 0')

        url = requests.get(f'https://api.currencyapi.com/v3/latest?apikey='
                           f'cur_live_DelTUoaNnnyCxpAIlamE2VFVZD0i9XoYso3Goo9D&currencies='
                           f'{TIKERS[base]}%2C{TIKERS[quote]}')

        js = json.loads(url.content)
        price = js['data'][TIKERS[quote]]['value'] / js['data'][TIKERS[base]]['value'] * float(amount)
        return price

    @staticmethod
    def get_current_currency():
        """

        :return: List [code currency , value currency]
        """
        url = requests.get(f'https://api.currencyapi.com/v3/latest?apikey='
                           f'cur_live_DelTUoaNnnyCxpAIlamE2VFVZD0i9XoYso3Goo9D&currencies='
                           f'{TIKERS['доллар']}%2C{TIKERS['евро']}%2C{TIKERS['рубль']}')

        current_currencies = json.loads(url.content)
        return [f'{currency['code']} : {currency['value']}' for j in current_currencies.values()\
                for currency in j.values() if isinstance(currency, dict)]
