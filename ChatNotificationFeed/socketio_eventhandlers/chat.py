from flask_jwt_extended import jwt_required, get_jwt_identity

from ..main import sio

@sio.event
@jwt_required
def connect(sid, environ, auth):
    print(f"Client {sid} connected...")
    # The user should enter his personal room on connection
    sio.enter_room(sid, get_jwt_identity()['id'])

# @sio.event
# def enter_personal_room(sid, data):
#     sio.enter_room(sid, room=data['user_id'])
#     print(f"Client {data} entered their personal room..")

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

    # sio.call('join conversation', data['conv_id'], room=data['receiver_id'])

    sio.emit('join conversation', data['conv_id'], room=data['receiver_id'])

    sio.emit('message', data, room=data['conv_id'])


@sio.event
def post(sid, data):
    print(f"Received post from {sid} in post namespace, {data}")

    sio.emit("post", data)