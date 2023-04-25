import hashlib
import random
import string
import sqlite3
import datetime
import secrets

def generate_random_string(length=32):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def generate_id():
    raw = generate_random_string()
    random_id = hashlib.sha256(raw.encode('utf-8')).hexdigest()[:32]
    return random_id

def create_undefined_table(HALLWAYDB_PATH, HALLWAY_NAME):
    conn = sqlite3.connect(HALLWAYDB_PATH)
    cursor = conn.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {HALLWAY_NAME} (
                        chatRoomId TEXT PRIMARY KEY NOT NULL,
                        userOne TEXT NOT NULL,
                        userTwo TEXT NOT NULL, 
                        lenUsers INT NOT NULL)''')
    conn.commit()
    conn.close()

def get_data(DB_PATH, column_name, session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'SELECT {column_name} FROM users WHERE sessionID = ?', [session_id])
    row = cursor.fetchone()
    conn.close()

    return row[0]


def roomId (HALLWAYDB_PATH, hallway_name, username):
    conn = sqlite3.connect(HALLWAYDB_PATH)
    cursor = conn.cursor()

    query = f"""SELECT chatRoomID
                FROM {hallway_name}
                WHERE userOne = ?
                UNION
                SELECT chatRoomID
                FROM {hallway_name}
                WHERE userTwo = ?
                LIMIT 1"""

    cursor.execute(query, [username, username])
    chatRoomID = cursor.fetchone()[0]
    conn.close()

    return chatRoomID

import sqlite3

def check_for_user_in_database(DB_PATH, username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Use parameterized query to prevent SQL injection
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    room = None

    for table in tables:
        table_name = table[0]
        try:
            # Use UNION to combine two SELECT queries into one
            cursor.execute(f"SELECT * FROM {table_name} WHERE userOne = ? UNION SELECT * FROM {table_name} WHERE userTwo = ?", (username, username))
            result = cursor.fetchone()
            if result is not None:
                room = result
                hallway_name = table_name
                break
        except sqlite3.OperationalError as e:
            # Handle specific exceptions that might occur
            print(f"Error executing query on table {table_name}: {e}")
        except sqlite3.ProgrammingError as e:
            print(f"Error in SQL syntax on table {table_name}: {e}")

    conn.close()
    if room is None:
        return False, None, None

    return True, room[0], hallway_name

def remove_user_from_room(DB_PATH, table_name, username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(f"DELETE FROM {table_name} WHERE userOne = ? OR userTwo = ?", (username, username))
    except sqlite3.OperationalError as e:
        print(f"Error executing query on table {table_name}: {e}")
    except sqlite3.ProgrammingError as e:
        print(f"Error in SQL syntax on table {table_name}: {e}")

    conn.commit()
    conn.close()
