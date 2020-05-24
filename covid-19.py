import telebot
import threading
from functools import wraps
from telebot import types
from covid import Covid
import datetime
import time
import string
bot = telebot.TeleBot('1124830353:AAGcKzwJ0VmgVS8ycmI5Vb8qIpYtcyxI70E')
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Armenia')
    btn2 = types.KeyboardButton('World')
    markup.add(btn1, btn2)
    messageText = f"Ողջույն <b>{message.from_user.first_name}</b>! Կորոնավիրուսի մասին վերջին տվյալները ստանալու համար ուղարկեք երկրի անունը (լատինատառերով), օրինակ՝ Armenia, Russia, Italy, Iran և այլն։"
    bot.send_message(message.chat.id, messageText, parse_mode='html', reply_markup=markup)

def get_recovered_percent(recovered, deaths):
    return round(recovered*100/(deaths+recovered), 2)

def get_deaths_percent(recovered, deaths):
    return round(deaths*100/(deaths+recovered), 2)

def get_active_cases_percent(active, confirmed):
    return round(active*100/confirmed, 2)

@bot.message_handler(content_types=['text'])
def mess(message):
    getMessage=message.text.strip().lower()
    covid = Covid(source="worldometers")
    if getMessage=="world":
        data={'active':covid.get_total_active_cases(),'confirmed':covid.get_total_confirmed_cases(),'deaths':covid.get_total_deaths(),'recovered':covid.get_total_recovered(),'last_update':int(round(time.time()*1000))}
        replyMessage = f"COVID-19-ի վերջին տվյալները Աշխարհում։ Աշխարհում կա <b>{data['confirmed']}</b> վարակված անձ որոնցից ապաքինվել է <b>{data['recovered']}({get_recovered_percent(data['recovered'], data['deaths'])}%)</b> մարդ, մահացել <b>{data['deaths']}({get_deaths_percent(data['recovered'], data['deaths'])}%)</b>-ը և այժմ բուժում է ստանում <b>{data['active']}({get_active_cases_percent(data['active'], data['confirmed'])}%)</b> մարդ։"
        data.clear()
        bot.send_message(message.chat.id, replyMessage, parse_mode='html')
    else:
        try:
            print(getMessage)
            data = covid.get_status_by_country_name(getMessage)
            print(getMessage, data)
            replyMessage = f"COVID-19-ի վերջին տվյալները <b>{string.capwords(getMessage)}</b>-ում։ Երկրում կա <b>{data['confirmed']}</b> վարակված անձ որոնցից ապաքինվել է <b>{data['recovered']}({get_recovered_percent(data['recovered'], data['deaths'])}%)</b> մարդ, մահացել <b>{data['deaths']}({get_deaths_percent(data['recovered'], data['deaths'])}%)</b>-ը և այժմ բուժում է ստանում <b>{data['active']}({get_active_cases_percent(data['active'], data['confirmed'])}%)</b> մարդ։ Ընդհանուր կատարվել է <b>{data['total_tests']}</b> թեստավորում (յուրաքանչյուր մեկ միլիոն բնակչին ընկնող թեստավորումների քանակը <b>{data['total_tests_per_million']}</b> է)։ Վերջին մեկ օրում գրանցվել է <b>{data['new_cases']}</b> նոր դեպք, մահացել է <b>{data['new_deaths']}</b> մարդ։ Յուրաքանչյուր մեկ միլիոն բնակչից վարակվել է <b>{data['total_cases_per_million']}</b> մարդ, մահացել <b>{data['total_deaths_per_million']}</b>-ը։ Վարակվածների թվի տոկոսային աճը՝ <b>{round((data['new_cases']/(data['confirmed']-data['new_cases']))*100, 2)}%</b>"
            data.clear()
            bot.send_message(message.chat.id, replyMessage, parse_mode='html')
        except Exception as error:
            print('Error: ' + repr(error))
            replyMessage = "Երկրի անունը սխալ է!"
            bot.send_message(message.chat.id, replyMessage, parse_mode='html')

bot.polling(none_stop=True)