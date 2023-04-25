from flask import Blueprint, session, request
import sqlite3
import datetime
import secrets

feed = Blueprint('feed', __name__)
FEED_DB = "./database/feed.sqlite"

def create_undefined_table(path):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()

        create_table_query = '''CREATE TABLE IF NOT EXISTS feeds (
                                    id TEXT PRIMARY KEY NOT NULL, 
                                    username TEXT NOT NULL,
                                    type TEXT NOT NULL,
                                    message TEXT NOT NULL,
                                    sentTime TEXT NOT NULL)'''
        cursor.execute(create_table_query)

        create_trigger_query = '''CREATE TRIGGER IF NOT EXISTS delete_expired_feeds
                                  BEFORE DELETE ON feeds
                                  BEGIN
                                      DELETE FROM feeds WHERE sentTime < datetime('now', '-1 day');
                                  END;'''
        cursor.execute(create_trigger_query)

        conn.commit()

@feed.route('/get')
def get_feed():
    data = request.args.to_dict()
    type_one = data.get('typeOne')
    type_two = data.get('typeTwo')
    type_three = data.get('typeThree')

    create_undefined_table(FEED_DB)

    with sqlite3.connect(FEED_DB) as conn:
        cursor = conn.cursor()

        feed_data = []
        for feed_type in [type_one, type_two, type_three]:
            query = '''SELECT id, username, type, message
                       FROM feeds
                       WHERE type = ? AND sentTime > datetime('now', '-1 day')'''
            cursor.execute(query, (feed_type,))
            feed_data += cursor.fetchall()

    return {'feeds': [{'id': row[0], 'username': row[1], 'type': row[2], 'message': row[3]} for row in feed_data]}


@feed.route('/send', methods=['POST'])
def send_feed():
    data = request.get_json()
    username = data['user']
    feed_type = data['type']
    message = data['content']
    
    create_undefined_table(FEED_DB)

    id = secrets.token_hex(8)
    sent_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with sqlite3.connect(FEED_DB) as conn:
        cursor = conn.cursor()
        query = '''INSERT INTO feeds
                   (id, username, type, message, sentTime)
                   VALUES (?, ?, ?, ?, ?)'''
        cursor.execute(query, (id, username, feed_type, message, sent_time))
        conn.commit()

    return {'response': 'success'}