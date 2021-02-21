import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('0e7374aafd17b5d621eebd947ee68013', config_dict)
mgr = owm.weather_manager()
bot = telebot.TeleBot("1658263591:AAFQVYNs1msUdKykXDTpJw3GjQY1O-Rxu8A")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет!\nИспользуйте "/" для показа команд')


@bot.message_handler(commands=['weather'])
def weather(message):
    # place = 'санкт-петербург'
    # w = mgr.weather_at_place(place).weather
    # temperature = w.temperature('celsius')
    # answer = f'На улице {w.detailed_status}, {round(temperature["temp"])}°C.\nОщущается как {round(temperature["feels_like"])}°C'
    msg = bot.send_message(message.chat.id, 'Где вы хотите узнать погоду?\nНапишите страну/город')
    bot.register_next_step_handler(msg, process_region_step)


def process_region_step(message):
    try:
        w = mgr.weather_at_place(message.text).weather
        temperature = w.temperature('celsius')
        answer = f'На улице {w.detailed_status}, {round(temperature["temp"])}°C.\nОщущается как {round(temperature["feels_like"])}°C'
        bot.send_message(message.chat.id, answer)
        with open('weather.txt', 'a', encoding='utf-8') as f:
            f.write(f'{message.from_user.username} - {message.text}\n')
    except Exception:
        bot.reply_to(message, 'oops, это не страна и не город')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.lower() in ('паша', 'павел'):
        bot.send_message(message.from_user.id, 'СОЗДАТЕЛЬ')
    elif message.text.lower() == 'марина':
        bot.send_message(message.from_user.id, 'Клоун!😉')
    elif message.text.lower() in ('ирина', 'ира'):
        bot.send_message(message.from_user.id, 'Ещё один!😝')
    elif message.text.lower() == 'марина':
        bot.send_message(message.from_user.id, 'Клоун!😉')
    else:
    	bot.send_message(message.chat.id, message.text)
    	# bot.reply_to(message, message.text)


print('работаем')
bot.polling(none_stop=True)
