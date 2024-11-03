from flask import Flask
from telebot import TeleBot
from config import bot_token, db_url
from database_server import Database

from g4f.client import Client

app = Flask(__name__)
# app.config['TEMPLATES_AUTO_RELOAD'] = True
bot = TeleBot(bot_token)
db = Database(db_url)
chatgpt = Client()