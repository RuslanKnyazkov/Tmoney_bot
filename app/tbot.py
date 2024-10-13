import telebot
from config import TOKEN, TIKERS
from extensions import (APIException,
                        Currency,
                        set_declensions)

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def get_insturtion(message) -> None:
    bot.reply_to(message, text=f'Для получения результата конвертации необходимо '
                               f'ввести <конвертируемую валюту>  <необходимую валюту> <ее количество>\n'
                               f'Пример: <Рубль> <Доллар> <1>')


@bot.message_handler(commands=['help'])
def get_command(message) -> None:
    """
    Show command for bot.
    """
    bot.reply_to(message, text='Что бы узнать имеющиеся валюты для конвертации , напишите /values \n'
                               'Шаблон необходимый для конвертации /start \n'
                               'Узнать текущий курс валют /course')


@bot.message_handler(commands=['values'])
def get_values(message) -> None:
    """
    Show available currency.
    """
    items = 'Доступные валюты: \n'
    for tiker in TIKERS.keys():
        items += f'- {tiker.title()}\n'
    bot.reply_to(message, text = items)

@bot.message_handler(commands=['course'])
def show_course(message) -> None:
    """
    Show current course.
    """
    currensy = Currency().get_current_currency()
    text = '\n'.join(currensy)
    bot.reply_to(message, text=f'Текущий курс: \n {text}')

@bot.message_handler(content_types=['text'])
def converting(message) -> None:
    """
    Function for conversion currencies.
    """
    try:
        if len(message.text.split(' ')) != 3:
            raise APIException('Неправильный формат введенной информации')
        base, quote, amount = message.text.lower().split(' ')
        total_result = Currency().get_price(base, quote, amount)

    except APIException:
        bot.reply_to(message, text=f'Введенная вами {message.text} не может быть обработана '
                                   f'воспользуйтесь командой /help')
    except Exception as e:
        bot.reply_to(message, f'Ошибка со стороны сервера {e}')
    else:
        bot.reply_to(message, text=f'Стоимость {set_declensions(num=amount,
                                                                currency_base=base,
                                                                currency_quote=quote)} - {round(total_result, 2)}')


if __name__ == '__main__':
    bot.infinity_polling(timeout= None)