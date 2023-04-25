import datetime
from email import message
import sqlite3
import secrets
from app.hallway.utils import create_undefined_table, get_data, check_for_user_in_database, remove_user_from_room
from flask import current_app, session
from flask_socketio import emit, join_room, leave_room
from flask_socketio import SocketIO
import json
from flask import request

socketio = SocketIO(logger=False, engineio_logger=False)

HALLWAYDB_PATH = "./database/hallway.sqlite"
DB_PATH = "./database/login_info.sqlite"


@socketio.on("join")
def on_join(data):
    hallway_name = data["hallway"]
    session["hallWayName"] = hallway_name
    session_id = session.get("id")
    username = session.get('userName')
    create_undefined_table(HALLWAYDB_PATH, hallway_name)

    current_app.logger.info(
        f"User with username: {username} trying to join hallway: {hallway_name}."
    )

    # Get the list of rooms the user is in
    try:
        inRoom, roomName, hallName = check_for_user_in_database(HALLWAYDB_PATH, username)
        if inRoom:
            current_app.logger.info(f"The user with session {session_id} is in room: {roomName}")
            emit('message', {'room': roomName, 'text': f'{username}! leave the current room first!!'}, room=roomName, broadcast=True)
            return None
        else:
            current_app.logger.info(f"The user with session {session_id} is not in any rooms.")
    except KeyError:
        current_app.logger.info(f"The user with session {session_id} is not in any rooms.")

    # Check if there is an empty room available in the hallway
    with sqlite3.connect(HALLWAYDB_PATH) as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM {hallway_name} WHERE lenUsers = 1 LIMIT 1"
        cursor.execute(query)
        row = cursor.fetchone()

        if row is None:
            # If there are no empty rooms, create a new one
            chatroomID = "room_" + secrets.token_hex(8)
            session["chatRoomID"] = chatroomID
            join_room(chatroomID)

            current_app.logger.info(
                f"User with username {username} created a new chatroom with ID {chatroomID} in hallway {hallway_name}."
            )

            # Insert the new room into the hallway database
            new_room_query = f"""INSERT INTO {hallway_name} (
                        chatRoomID,
                        userOne,
                        userTwo,
                        lenUsers)
                        VALUES (?, ?, ?, ?)"""
            cursor.execute(new_room_query, [chatroomID, username, "", 1])
            conn.commit()

            emit(
                "message", {"room": chatroomID, "text": username + " created new chatroom"}
            )
        else:
            # If there is an empty room, join that room
            chatroomID = row[0]
            session["chatRoomID"] = chatroomID
            join_room(chatroomID)
            current_app.logger.info(
                f"User with username {username} joined chatroom with ID {chatroomID} in hallway {hallway_name}."
            )

            sql_query = f"""UPDATE {hallway_name}
                            SET userTwo = ?, lenUsers = ?
                            WHERE chatRoomID = ?"""
            cursor.execute(sql_query, [username, 2, row[0]])
            conn.commit()

        emit("message", {"room": chatroomID, "text": username + " joined the chat"}, room=chatroomID, broadcast=True)
        emit("message", {"room": chatroomID, "text": "let's go"}, room=chatroomID, broadcast=True)


@socketio.on("leave")
def on_leave(data):
    try:
        hallway_name = session.get("hallWayName")
        session["chatRoomId"] = ""
        username = session.get("userName")
        chatRoomID = session.get("chatRoomID")

        if chatRoomID == None:
            return {'response', 'operation failed!'}

        emit(
            "message",
            {"room": chatRoomID, "text": username + " left the chat"},
            room=chatRoomID,
            broadcast=True,
        )

        leave_room(chatRoomID)
        remove_user_from_room(HALLWAYDB_PATH, hallway_name, username)

        session['hallWayName'] = None
        session['chatRoomId'] = None

        current_app.logger.info(
            f"User {username} left the chat in hallway {hallway_name}"
        )

    except Exception as e:
        current_app.logger.error(f"Error in on_leave: {e}")


@socketio.on('disconnect')
def on_disconnect():
    try:
        hallway_name = session.get("hallWayName")
        session["chatRoomId"] = ""
        username = session.get("userName")
        chatRoomID = session.get("chatRoomID")

        if chatRoomID == None:
            return {'response', 'operation failed!'}

        emit(
            "message",
            {"room": chatRoomID, "text": username + " left the chat"},
            room=chatRoomID,
            broadcast=True,
        )

        leave_room(chatRoomID)
        remove_user_from_room(HALLWAYDB_PATH, hallway_name, username)

        session['hallWayName'] = None
        session['chatRoomId'] = None

        current_app.logger.info(
            f"User {username} left the chat in hallway {hallway_name}"
        )

    except Exception as e:
        current_app.logger.error(f"Error in on_leave: {e}")

@socketio.on("message")
def on_message(data):
    try:
        data = json.loads(data)
        message = data["message"]
        session_id = session.get("id")
        username = get_data(DB_PATH, "userName", session_id)
        chatRoomID = session.get("chatRoomID")
        emit(
            "message",
            {"text": message, "sender": username, "time": str(datetime.datetime.now().strftime("%H:%M"))},
            room=chatRoomID,
            broadcast=True,
        )

        # Log the message, sender, and time using current_app.logger
        current_app.logger.info(
            f"Received message: '{message}'' from user '{username}' at {datetime.datetime.now()} in chatRoom '{chatRoomID}'"
        )
    except json.JSONDecodeError as e:
        # Log the specific error message when the JSON parsing fails
        current_app.logger.error(f"Error parsing message: {e}")
    except Exception as e:
        # Log any other exceptions that occur during the function
        current_app.logger.error(f"Error in on_message: {e}")
