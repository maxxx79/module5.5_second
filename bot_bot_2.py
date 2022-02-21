
import telebot
from bot_config import keys, TOK
from extension3 import ConversionExeption, CryptoConverter

bot = telebot.TeleBot(TOK)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = '       Чтобы начать работу,\n введи команду боту через пробел:' \
           '\n\n <имя валюты> ' \
           '\n\n <в какую валюту перевести> ' \
           '\n\n <количество переводимой валюты>'
    text2 = '<Увидеть список ' \
            'всех доступных валют: /values >'
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, text2)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionExeption('Количество параметров не равно 3.')

        quote, base, amount = values

        total_price = CryptoConverter.convert(quote, base, amount)
    except ConversionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_price}'
        bot.send_message(message.chat.id, text)

bot.polling()