from telebot import TeleBot, types
import random

bot = TeleBot('5694054533:AAGVrj58icZPu0L0_3XEVwa3pP1tLO1TGkU')


btn = types.InlineKeyboardButton(text='Кнопка', web_app=types.WebAppInfo(url='https://form-for-revenant.vercel.app/event/13'))
kb = types.InlineKeyboardMarkup().add(btn)
bot.send_message(5061120370, str(random.randint(0, 100)), reply_markup=kb)