import datetime, sqlite3
from flask import redirect, render_template, session, Blueprint, current_app

from app.hallway.utils import get_data

redirect_ = Blueprint('redirect', __name__)
DB_PATH = './database/login_info.sqlite'

@redirect_.route('/personality_test')
def show_personality_test():
    if not session.get('id'):
        current_app.logger.info("Session id not found")
        return redirect("/", 301)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE sessionID = ?', [session.get('id')])
    row = cursor.fetchone()
    conn.close()

    headers = [header[0] for header in cursor.description]
    timedelta = datetime.datetime.now() - datetime.datetime.strptime(row[headers.index('sessionExpiry')], '%Y-%m-%d %H:%M:%S.%f') 
    if timedelta.total_seconds() > 3600:
        return redirect("/", 301)

    if row[headers.index('personalityType')]:
        return redirect("/dashboard")
    
    return render_template('personality_test.html')

@redirect_.route('/dashboard')
def show_dashboard():
    username = session.get('userName')
    ptype = get_data(DB_PATH, "personalityType", session.get("id"))
    return render_template("dashboard.html", username=username, ptype = ptype)

@redirect_.route('/chat')
def chat():
    username = session.get('userName')
    print(session.get('id'))
    pType = get_data(DB_PATH, "personalityType", session.get("id"))
    # print("personality of username ", username, " is ", pType);
    return render_template("chat.html", username=username, personalityType = pType)

@redirect_.route('/reels')
def reels():
    username = session.get('userName')
    return render_template("reels.html", username=username)

@redirect_.route('/profile')
def profile():
    username = session.get('userName')
    return render_template("profile.html", username=username)