import telebot
from telebot import types
from covid import Covid
import datetime
import time
import string
covid = Covid(source="worldometers")
bot = telebot.TeleBot('1124830353:AAE5tDXSRBdXBGI-wzdx6MIR0MXE98Zo8Dw')
data = {}

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
    if getMessage=="world":
        data={'active':covid.get_total_active_cases(),'confirmed':covid.get_total_confirmed_cases(),'deaths':covid.get_total_deaths(),'recovered':covid.get_total_recovered(),'last_update':int(round(time.time()*1000))}
        print(data)
    else:
        data = covid.get_status_by_country_name(getMessage)
        #<br>Վերջին Թարմացումը: <b> {datetime.datetime.fromtimestamp(data['last_update']/1000.0)}</b>
    replyMessage = f"COVID-19-ի վերջին տվյալները <b>{string.capwords(message.text)}-ում</b><br>Վարակված: <b>{data['confirmed']}</b><br>Ապաքինված: <b>{data['recovered']}</b><br>Մահացած: <b>{data['deaths']}</b><br>Վարակակիր: <b>{data['active']}</b>"
    bot.send_message(message.chat.id, replyMessage, parse_mode='html')

bot.polling(none_stop=True)