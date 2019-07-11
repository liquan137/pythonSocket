from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    send(message)
@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    return str(json)

@app.route('/')
def home():
    return render_template('demo.html')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)
