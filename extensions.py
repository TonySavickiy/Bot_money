import json
import requests
from config import exchanges, TOKEN_SEC, exchanges_r


#Создаём собственное исключение, которое в дальнейшем будем рэйзить и обрабатывать 
class ConvertExeption(Exception):
    pass

#Описание основной функции конвертации валют.
class MoneyChange:    
    @staticmethod
    def get_price(base: str, quote: str, amount):
        try:
            # Проверка на доступность 1-й валюты
            base_key = exchanges[base.lower()]
        except KeyError:
            raise ConvertExeption(f"Валюта '{base}' не найдена!")

        try:
            # Проверка на доступность 2-й валюты
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise ConvertExeption(f"Валюта '{quote}' не найдена!")
            
            # Проверка на равенство конвертируемых валют
        if base_key == quote_key:
            raise ConvertExeption(f'Невозможно перевести одинаковые валюты "{base}" и "{quote}"!')
        
        # Проверка на корректность введенной суммы(должно быть int\float)
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertExeption(f'Не удалось обработать количество: "{amount}", кол-во должно быть цифрой!')

        # После прохода проверок, генерируем GET запрос к API
        r = requests.get(f'https://openexchangerates.org/api/latest.json?app_id={TOKEN_SEC}')
        
        # Полученный ответ конвертируем с помощью json
        resp = json.loads(r.content)
        
        # Костыль описан в описании, в файле main.py
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
