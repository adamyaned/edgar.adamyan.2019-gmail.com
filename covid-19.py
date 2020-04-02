import telebot
from telebot import types
from covid import Covid
import datetime
import time
import string
bot = telebot.TeleBot('1124830353:AAE5tDXSRBdXBGI-wzdx6MIR0MXE98Zo8Dw')

@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton('Armenia')
	btn2 = types.KeyboardButton('World')
	markup.add(btn1, btn2)
	messageText = f"Ողջույն <b>{message.from_user.first_name}</b>! Կորոնավիրուսի մասին վերջին տվյալները ստանալու համար ուղարկեք երկրի անունը (լատինատառերով), օրինակ՝ Armenia, Russia, Italy, Iran և այլն։"
	bot.send_message(message.chat.id, messageText, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def mess(message):
    getMessage=message.text.strip().lower()
    covid = Covid(source="worldometers")
    countries = covid.list_countries()
    if getMessage=="world":
        data={'active':covid.get_total_active_cases(),'confirmed':covid.get_total_confirmed_cases(),'deaths':covid.get_total_deaths(),'recovered':covid.get_total_recovered(),'last_update':int(round(time.time()*1000))}
        replyMessage = f"COVID-19-ի վերջին տվյալները Աշխարհում։ Աշխարհում կա <b>{data['confirmed']}</b> վարակված անձ որոնցից ապաքինվել է <b>{data['recovered']}({round(data['recovered']*100/data['confirmed'], 2)}%)</b> մարդ, մահացել <b>{data['deaths']}({round(data['deaths']*100/data['confirmed'], 2)}%)</b>-ը և այժմ բուժում է ստանում <b>{data['active']}({round(data['active']*100/data['confirmed'], 2)}%)</b> մարդ։"
        data.clear()
    elif getMessage in countries:
        data = covid.get_status_by_country_name(getMessage)
        replyMessage = f"COVID-19-ի վերջին տվյալները <b>{string.capwords(message.text)}</b>-ում։ Երկրում կա <b>{data['confirmed']}</b> վարակված անձ որոնցից ապաքինվել է <b>{data['recovered']}({round(data['recovered']*100/data['confirmed'], 2)}%)</b> մարդ, մահացել <b>{data['deaths']}({round(data['deaths']*100/data['confirmed'], 2)}%)</b>-ը և այժմ բուժում է ստանում <b>{data['active']}({round(data['active']*100/data['confirmed'], 2)}%)</b> մարդ։ Վերջին մեկ օրում գրանցվել է <b>{data['new_cases']}</b> նոր դեպք, վարակվածների թվի տոկոսային աճը՝ <b>{round((data['new_cases']/(data['confirmed']-data['new_cases']))*100, 2)}%</b>"
        data.clear()
    else:
        replyMessage = "Երկրի անունը սխալ է!"
        
    bot.send_message(message.chat.id, replyMessage, parse_mode='html')

bot.polling(none_stop=True)