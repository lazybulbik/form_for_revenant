from loader import app
from flask import Flask, render_template, request, redirect
from database_server import Database
from config import db_url
import utils


@app.route('/api/users_notify', methods=['POST'])
def users_notify():
    data = request.get_json()

    user_id = data['user_id']
    event_id = data['event_id']

    db = Database(db_url)

    event_data = eval(db.get_data(table='events', filters={'id': event_id})[0]['data'])
    notify = event_data['notify']

    result = {
        '2': user_id in notify['2'],
        '4': user_id in notify['4'],
        '24': user_id in notify['24'],
        '72': user_id in notify['72'],
        '168': user_id in notify['168'],
    }

    del db

    return result    


@app.route('/api/set_notify', methods=['POST'])
def set_notify():
    data = request.get_json()

    user_id = data['user_id']
    event_id = data['event_id']
    notify_id = data['notify']

    db = Database(db_url)

    event_data = eval(db.get_data(table='events', filters={'id': event_id})[0]['data'])


    if user_id in event_data['notify'][notify_id]:
        event_data['notify'][notify_id].remove(user_id)
        db.update_data(data={'data': str(event_data)}, filters={'id': event_id}, table='events')
        del db
        return {'status': 'remove'}
    else:
        event_data['notify'][notify_id].append(user_id)
        db.update_data(data={'data': str(event_data)}, filters={'id': event_id}, table='events')
        del db
        return {'status': 'add'}