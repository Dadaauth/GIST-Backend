from flask import Flask
import socketio


app = Flask(__name__)
sio = socketio.Server(async_mode="threading")
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

@sio.event
def connect(sid, environ, auth):
    # I want the user to enter their personal room back on reconnect.
    print(f"Client {sid} connected...")

@sio.event
def enter_personal_room(sid, data):
    sio.enter_room(sid, room=data['user_id'])
    print(f"Client {data} entered their personal room..")

@sio.event
def disconnect(sid):
    print(f"Client {sid} disconnected...")

@sio.event
def enter_conversation_room(sid, data):
    # Enter the conversation room specifically for the conversation participants
    sio.enter_room(sid, room=data.get('conv_id'))
    print(f"client {data['user']} joined a conversation room")

@sio.event
def message(sid, data):
    print(f"Received message from {sid} in two-user chat: {data}")

    # sio.enter_room(sid, room=data['receiver_id'])
    sio.emit('join conversation', data['conv_id'], room=data['receiver_id'])
    # sio.leave_room(sio, room=data['receiver_id'])

    sio.emit('message', data, room=data['conv_id'])

if __name__ == "__main__":
    app.run(port=5004, debug=True)