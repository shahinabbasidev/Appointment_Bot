from telebot import TeleBot,types
from dotenv import load_dotenv
import os
import query

load_dotenv()
api_token = os.getenv("API_TOKEN")
bot = TeleBot(api_token)

user_state = {}

admins =['474476386']
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.username
    query.insert_db(user_id,user_name)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Available Services','My Appointment')
    if user_id in admins:
        markup.row('Add Appointment')
    bot.send_message(user_id,'Welcome to my bot\n Please choose an options', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Available Services')
def choose_services(message):
    services = query.show_available_services()
    inline_key = types.InlineKeyboardMarkup()
    for service_id , service_name in services:
        inline_key.add(types.InlineKeyboardButton(service_name, callback_data=f'service_{service_id}'))
    bot.send_message(message.chat.id, 'choose service:', reply_markup=inline_key)


@bot.callback_query_handler(func= lambda call: call.data.startwith('service_'))
def choose_data(call):
    service_id = int(call.data.split('_')[1])
    user_state[call.from_user.id]= {'service_id':service_id}
    dates = query.get_date(service_id)

    inline_key = types.InlineKeyboardMarkup()
    for d in dates:
        btn = types.InlineKeyboardButton(d, callback_data=f'date_{d}')
        inline_key.add(btn)
    bot.send_message(call.message.chat.id, 'Choose a date:', reply_markup=inline_key)

@bot.callback_query_handler(func= lambda call: call.data.startswith('date_'))
def choose_data(call):
    date = int(call.data.split('_')[1])
    user_id = call.from_user.id
    user_state[user_id]['date'] = date
    service_id = user_state[user_id]['service_id']

    times = query.get_time(service_id, date)
    inline_key = types.InlineKeyboardMarkup()

    for slot_id, slot_time in times:
        btn = types.InlineKeyboardButton( text=slot_time, callback_data= f'time_{slot_id}')
        inline_key.add(btn)
    bot.send_message(call.message.chat.id, 'Choose a time', reply_markup=inline_key)

@bot.callback_query_handler(func= lambda call: call.data.startswith('time_'))
def confirm(call):
    slot_id = int(call.data.split('_')[1])
    user_id = str(call.from_user.id)

    query.book_appointment(user_id, slot_id)
    query.update_slot_status(slot_id)

    bot.send_message(call.message.chat.id, 'Appointment reserved successfully')
    user_state.pop(call.from_user.id, None)






















bot.infinity_polling()