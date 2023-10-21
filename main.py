"""
В моём варианте бота использован некий костыль в виде отношения курса к курсу, если базовая валюта отлична от USD.

Такое решение было принято в связи с тем, что на текущий момент(10.2023) в двух 
из 2х доступных вариантов api(https://openexchangerates.org/ и https://exchangeratesapi.io/)
в бесплатной версии, в качестве base доступен только USD.

Я приложу в файл (else.py) вариант с использованием двух аргументов при отправке запроса на https://exchangeratesapi.io/

Сам же я решил использовать api от сервиса https://openexchangerates.org/


"""


import telebot
from extensions import APIException, MoneyChange
from config import TOKEN_TG, money_list
import traceback


bot = telebot.TeleBot(TOKEN_TG)


#Описание инструкции
@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = '''Чтобы начать работу выведите команду боту в следующем формате:
    Имя валюты(цену которой вы хотите узнать).
    Имя валюты(в которой будет представлен результат).
    Кол-во валюты для измерения.
    Данные необходимо вводить через пробел, без знаков припинания.
Доступные валюты по команде: /value'''
    bot.reply_to(message, text)

    
@bot.message_handler(commands=['value'])
def get_value(message: telebot.types.Message):
    text = 'Список доступных валют:'
    box ='\n'.join(money_list)
    bot.reply_to(message, text+'\n'+box)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!(Введите 3 значения без знаков припинания)')
        
        answer = MoneyChange.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}" )
    else:
        bot.reply_to(message,answer)

bot.polling()
