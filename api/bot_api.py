from loader import app
from flask import Flask, render_template, request, redirect
from database_server import Database
from config import db_url
import utils
import requests

from datetime import datetime


@app.route('/api/get_bot_username')
def get_bot_username():
    return {'username': utils.get_bot_username()}