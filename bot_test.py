from telebot import TeleBot, types

bot = TeleBot('5694054533:AAGVrj58icZPu0L0_3XEVwa3pP1tLO1TGkU')

kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='test', web_app=types.WebAppInfo(url='https://31a4-94-25-190-106.ngrok-free.app/event/13')))

bot.send_message(5061120370, 'test', reply_markup=kb)