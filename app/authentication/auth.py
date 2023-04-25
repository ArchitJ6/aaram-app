import datetime
import secrets
import sqlite3
from logging import *
import time
from flask import Blueprint, redirect, request, current_app, session

from app.authentication.utils import generate_user_hash

authentication = Blueprint('authentication', __name__)
DB_PATH = './database/login_info.sqlite'

@authentication.route('login/', methods=['POST'])
def login():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    user_name = request.json.get('userName')
    password = request.json.get('password')

    cursor.execute('SELECT 1 FROM users WHERE userName=? AND secretCode=? LIMIT 1', [user_name, password])

    row = cursor.fetchone()
    conn.close()

    if row is not None:
        session['id'] = secrets.token_hex(16)
        session['userName'] = user_name
        sql_query = "UPDATE users SET sessionID = ?, sessionExpiry = ? WHERE userName = ?"

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_query, (session.get('id'), datetime.datetime.now(), user_name))
        conn.commit()
        conn.close()

        current_app.logger.info(session.get('id'))
        current_app.logger.info('login successful ' + user_name)
        return 'success'

    current_app.logger.error('User not found')
    return 'User not found'


@authentication.route('signup/', methods=['POST'])
def signup():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        firstName TEXT NOT NULL, 
                        lastName TEXT NOT NULL, 
                        userName TEXT PRIMARY KEY NOT NULL, 
                        email TEXT NOT NULL, 
                        mobileNumber TEXT NOT NULL, 
                        dateOfBirth TEXT NOT NULL, 
                        secretCode TEXT NOT NULL,
                        sessionID TEXT,
                        sessionExpiry TEXT,
                        personalityType TEXT)''')

    data = request.json
    query = 'SELECT 1 FROM users WHERE userName=? OR email=? OR mobileNumber=? LIMIT 1'
    cursor.execute(query, (data['userName'], data['email'], data['mobileNumber']))
    row = cursor.fetchone()

    if row is not None:
        conn.close()
        current_app.logger.error('User already exists')
        return 'User already exists'

    query = '''INSERT INTO users (
                firstName, 
                lastName, 
                userName, 
                email, 
                mobileNumber, 
                dateOfBirth, 
                secretCode,
                sessionID,
                sessionExpiry,
                personalityType
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    cursor.execute(query, (
        data['firstName'], 
        data['lastName'], 
        data['userName'], 
        data['email'], 
        data['mobileNumber'], 
        data['dateOfBirth'], 
        data['password'],
        None,
        None,
        "",
    ))

    conn.commit()
    conn.close()

    current_app.logger.info("Success")
    return redirect("/")