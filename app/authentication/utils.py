import sqlite3
import hashlib

def generate_user_hash(username):

    conn = sqlite3.connect('./database/login_info.sqlite')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE userName=?", (username,))

    user_data = c.fetchone()

    user_string = ''.join(str(x) for x in user_data if x is not None)
    user_hash = hashlib.sha256(user_string.encode('utf-8')).hexdigest()[:32]

    conn.close()

    return user_hash