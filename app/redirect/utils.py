import sqlite3

def get_data(DB_PATH, column_name, session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'SELECT {column_name} FROM users WHERE sessionID = ?', [session_id])
    row = cursor.fetchone()
    conn.close()

    return row[0]