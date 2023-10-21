"""
В моём варианте бота использован некий костыль в виде отношения курса к курсу, если базовая валюта отлична от USD.

Такое решение было принято в связи с тем, что на текущий момент(10.2023) в двух 
из 2х доступных вариантов api(https://openexchangerates.org/ и https://exchangeratesapi.io/)
в бесплатной версии, в качестве base доступен только USD.

Я приложу в файл (else.py) вариант с использованием двух аргументов при отправке запроса на https://exchangeratesapi.io/

Сам же я решил использовать api от сервиса https://openexchangerates.org/


"""


import telebot
from extensions import ConvertExeption, MoneyChange
from config import TOKEN_TG, money_list
import traceback


bot = telebot.TeleBot(TOKEN_TG)


#Команды help\start
@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = '''Для начала работы, пожалуйста, введите наименования валют в следующем формате:
    Имя валюты(цену которой вы хотите узнать).
    Имя валюты(в которой будет представлен результат).
    Кол-во необходимой для измерения валюты.
    Данные необходимо вводить через пробел.
    
Список валют доступен по команде: /value '''
    bot.send_message(message.chat.id, text)


# Команда для получения списка доступных валют    
@bot.message_handler(commands=['value'])
def get_value(message: telebot.types.Message):
    text = 'Список доступных валют:'
    box ='\n'.join(money_list)
    bot.reply_to(message, text+'\n'+box)


# Захват сообщений от пользователя
@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    # Проверка на корректность введенных данных
    try:
        if len(values) != 3:
            raise ConvertExeption('Неверное количество параметров!(Введите 3 значения без знаков препинания)')
        
        answer = MoneyChange.get_price(*values)
    except ConvertExeption as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}" )
    else:
        bot.reply_to(message,answer)

bot.polling()
