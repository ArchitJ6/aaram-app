import json
import sqlite3, datetime
from flask import current_app, jsonify, session, Blueprint, redirect, render_template
import sqlite3
from sqlite3 import Error
from flask import g

from app.user_data.utils import get_db

profile = Blueprint('profile_data', __name__)
DB_PATH = './database/login_info.sqlite'

@profile.route("/<column_name>", methods=['GET'])
def get_user_data(column_name):

    authorized_columns = ['firstName', 'lastName', 'userName','sessionExpiry', 'personalityType']
    confidential_column = ['email', 'mobileNumber', 'dataOfBirth', 'secretCode', 'sessionID']

    if column_name in authorized_columns:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f'SELECT {column_name} FROM users WHERE sessionID = ?', [session.get('id')])
        row = cursor.fetchone()
        conn.close()

        if row == None:
            return jsonify({'response': 'Bad credentials'})
        elif row[0] == None:
            return jsonify({"response": "None"})

        current_app.logger.info(f"client with session id: {session.get('id')} requested column: {column_name}. Sent value: {row}.")
        return jsonify({column_name: row[0]})
    
    elif column_name in confidential_column:
        return jsonify({"response": "confidential data can't be requested."})
    else:
        return jsonify({"response": f"data with header name '{column_name}' not found."})

@profile.route("/<column_name>/<column_value>", methods=["POST"])
def set_data(column_name, column_value):
    print(column_name, column_value)
    if not session.get('id'):
        current_app.logger.info("Session id not found")
        return redirect("/", 302)

    try:
        conn = get_db(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE sessionID = ?', [session.get('id')])
        row = cursor.fetchone()

        print(1)
        headers = [header[0] for header in cursor.description]
        session_expiry_str = row[headers.index('sessionExpiry')]
        if session_expiry_str is not None:
            timedelta = datetime.datetime.now() - datetime.datetime.strptime(session_expiry_str, '%Y-%m-%d %H:%M:%S.%f')
        else:
            timedelta = datetime.timedelta(seconds=0)
        if timedelta.total_seconds() > 3600:
            return redirect("/", 302)

        print(2)
        query = f'''UPDATE users SET {column_name} = ? WHERE sessionID = ?'''
        cursor.execute(query, (column_value, session.get('id')))
        conn.commit()
    except Error as e:
        current_app.logger.error(f"Database error: {e}")
    finally:
        cursor.close()

    return redirect("/dashboard", 302)
