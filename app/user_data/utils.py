import sqlite3
from flask import g

def get_db(DB_PATH):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
    return db