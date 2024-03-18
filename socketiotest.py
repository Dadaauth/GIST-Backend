from flask import Flask
import socketio


app = Flask(__name__)
sio = socketio.Server(async_mode="threading")
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

@app.route('/here')
def here():
    return "Here", 200

@sio.event
def connect(sid, environ, auth):
    print("connect", sid)

@sio.event
def disconnect(sid):
    print("disconnect", sid)

@sio.event
def message_send(sid, data):
    sio.emit('message_received', data)

@sio.on('my custom event')
def another_event(sid, data):
    pass

@sio.on("*")
def any_event(event, sid, data):
    pass


if __name__ == "__main__":
    app.run(port=5004, debug=True)