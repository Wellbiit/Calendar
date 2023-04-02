from .database import session, User, Event
from flask import jsonify
import json


def create_json_from(obj):
    event_dict = obj.__dict__

    # Видаляємо ключ "_sa_instance_state", який додає SQLAlchemy
    event_dict.pop('_sa_instance_state', None)

    #Перетворюємо дату та час на рядки, щоб повернути їх користувачу
    event_dict['time'] = event_dict['time'].strftime('%H:%M')
    event_dict['date'] = event_dict['date'].strftime('%Y-%m-%d')

    json_string = json.dumps(event_dict)
    return json_string


def add_new_item(obj):
    session.add(obj)
    session.commit()


def check_if_user_exist(nickname: str):
    user = session.query(User).where(User.nickname == nickname).first
    return user


def get_events_by(date):
    events = session.query(Event).filter(Event.date == date, Event.user == 1).all() #.
    jsonified_events = []
    for event in events:
        jsonified_events.append(create_json_from(event))
    return jsonified_events


def delete_user(nickname):
    session.query(User).filter(User.nickname == nickname).delete()
