import json
import requests
from config import exchanges, TOKEN_SEC, exchanges_r


#Создаём собственное исключение, которое в дальнейшем будем рэйзить и обрабатывать 
class ConvertExeption(Exception):
    pass

#Описание основной функции
class MoneyChange:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise ConvertExeption(f"Валюта {base} не найдена!")

        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise ConvertExeption(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise ConvertExeption(f'Невозможно перевести одинаковые валюты {base}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertExeption(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'https://openexchangerates.org/api/latest.json?app_id={TOKEN_SEC}')
        resp = json.loads(r.content)
        if base_key !='USD':
            new_price = resp['rates'][quote_key] / resp['rates'][base_key] * amount
            new_price = round(new_price, 3)
            quote = exchanges_r[quote.lower()]
            base = exchanges_r[base.lower()]
            message =  f"Цена {amount} {base} : {new_price} {quote}"
            return message
        else:
            new_price = resp['rates'][quote_key] * amount
            new_price = round(new_price, 3)
            quote = exchanges_r[quote.lower()]
            base = exchanges_r[base.lower()]
            message =  f"Цена {amount} {base} : {new_price} {quote}"
            return message
