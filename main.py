from flask import Flask, render_template, request, redirect
from telebot import TeleBot, types
from database_server import Database
from config import db_url, bot_token
import utils

import time

from threading import Thread
import requests

from loader import app
from utils import add_user, can_send, escape_markdown, make_beautiful_text, send_message
import utils

from api import events_api, notify_api, profle_api, bot_api


@app.after_request
def disable_caching(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route('/form/<user_id>', methods=['GET', 'POST'])
def form(user_id):
    if request.method == 'POST':
        form_data = request.form.to_dict()
        
        send_message(user_id, make_beautiful_text(form_data))
        add_user(user_id)
        # print(form_data)

        return redirect('/finish')
    else:
        if can_send(user_id):
            return render_template('form.html')
        else:
            return redirect('/nope')
    

@app.route('/finish')
def finish():
    return render_template('finish.html')


@app.route('/nope')
def nope():
    return render_template('nope.html')


@app.route('/event')
def pass_def():
    args = request.args
    if args:
        event_id = args.get('tgWebAppStartParam')

        return redirect('/new_event/' + event_id)


@app.route('/new_event/<event_id>')
def events(event_id):
    anticash = time.time()
    return render_template('new_event.html', event_id=event_id, anticash=anticash)


@app.route('/events')
def events_list():
    return render_template('events.html')


@app.route('/profile/<user_id>')
def profile(user_id):
    return render_template('profile.html', user_id=user_id)


@app.route('/profile/<user_id>/achievements')
def profile_achievements(user_id):
    return render_template('profile_achievements.html', user_id=user_id)


@app.route('/')
def index():
    args = request.args
    if args:
        data = args.get('tgWebAppStartParam').split('_')

        if data[0] == 'event':
            event_id = data[1]
            return redirect(f'events')
        
        elif data[0] == 'profile':
            if len(data) > 1:
                user_id = data[1]
                return redirect(f'profile/{user_id}')
            
        elif data[0] == 'event_list':
            return redirect('events')
        

    return render_template('index.html')

@app.route('/chats')
def chats():
    return render_template('chats.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/api/is_admin', methods=['POST'])
def is_admin():
    data = request.get_json()

    user_id = data['user_id']
    event_id = data['event_id'] if 'event_id' in data else None

    db = Database(db_url)

    is_admin = utils.is_admin(user_id)

    if not event_id:
        return {'status': is_admin}

    event_data = db.get_data(table='events', filters={'id': event_id})[0]

    del db

    if is_admin == 'add_admin' and event_data['city'] == 'add':
        return {'status': True}
    
    return {'status': is_admin or event_data['creator'] == user_id}


if __name__ == '__main__':
    app.run(debug=True, port=5050)
