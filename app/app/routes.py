import requests
from datetime import datetime, timedelta
from app import app
from flask import jsonify
from app.database import User, Event, session
from .db_controls import add_new_item, get_events_by, delete_user
from flask import render_template, request, redirect, make_response
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


def convert_time_to_object(time):
    return datetime.strptime(time, "%H:%M").time()


def convert_date_to_object(date):
    return datetime.strptime(date, "%Y-%m-%d").date()


def add_event_to_database(event_data):
    event_data["time"] = convert_time_to_object(event_data["time"])
    event_data["date"] = convert_date_to_object(event_data["date"])
    event_data["user"] = 1
    event = Event(**event_data)
    add_new_item(event)


def create_response(status_code):
    response = make_response()
    response.status_code = status_code
    return response


@app.route("/create_event", methods=["POST"])
def create_event():
    data_from_request = request.get_json()
    print(data_from_request)
    try:
        add_event_to_database(data_from_request)
        response = make_response({"isAdded": True})
        response.status_code = 200
    except Exception as e:
        print(e)
        response = make_response({"isAdded": False, "exception": e})
        response.status_code = 500

    return response


@app.route("/get_events_by_date/<date>")
#TODO add jwt_required
def get_events_by_date(date):
    print(date)
    date = datetime.fromisoformat(date)
    data = get_events_by(date)
    response = make_response(data)
    return response


@app.route("/test")
def index():
    res = make_response({"ok?": "ok"})
    return res


@app.route("/login", methods=["POST"])
def login():
    data_from_request = request.get_json()

    name = data_from_request["nickname"]
    password = data_from_request["password"]

    user_check = session.query(User).where(User.nickname == name).first()

    if user_check:
        if check_password_hash(user_check.password, password):
            token = create_access_token(identity=user_check.id, expires_delta=timedelta(days=30))
            print(token)
            response = make_response(jsonify({"isLogged": True, "token": token}), 200)
            print(response)
            print(response.get_json())
            return response

    response = make_response({"isLogged": False}, 401)
    return response


@app.route("/signup", methods=["POST"])
def signup():
    data_from_request = request.get_json()
    print(data_from_request)
    name = data_from_request["nickname"]

    user_check = session.query(User).where(User.nickname == name).first()
    if user_check:
        response = make_response(jsonify({"isRegistered": False, "reason": "userExists"}), 409)
        return response

    data_from_request["password"] = generate_password_hash(data_from_request["password"])
    new_user = User(**data_from_request)
    add_new_item(new_user)
    response = make_response(jsonify({"isRegistered": True}), 200)
    return response


@app.route("/delete_user_by/<nickname>")
def delete_user_by(nickname):
    try:
        delete_user(nickname)
        response_json = {"isDeleted": True}
        status = 200
    except:
        response_json = {"isDeleted": False}
        status = 500

    response = make_response(response_json, status)
    return response

# @app.route("/test")
# @login_required
# def test():
#     import requests
#
#     response = requests.get('https://www.boredapi.com/api/activity')
#     print(response)
#     if response.status_code == 200:
#         data = response.json()["activity"]
#     else:
#         data = "ERROR"
#
#     return render_template("main.html", data=data)

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect("/")


# @app.errorhandler(404)
# @app.errorhandler(500)
# @app.errorhandler(405)
# def handler_error(e):
#     return render_template("custom_error.html", error=e.code)


# @login_manager.user_loader
# def load_user(user):
#     return session.query(User).get(int(user))
