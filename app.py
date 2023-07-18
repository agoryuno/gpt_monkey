from gevent import monkey
monkey.patch_all()

from gevent.event import Event
from gevent.timeout import Timeout

#from sqlalchemy import create_engine
#from sqlalchemy.pool import StaticPool
#from sqlalchemy.orm import scoped_session, sessionmaker

from gevent.event import Event
from gevent.timeout import Timeout

from flask import Flask, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO

#from database.database import Token, Base
from utils import get_config

app = Flask(__name__)
CORS(app)  # Add CORS support to allow cross-origin requests
app.config['SECRET_KEY'] = 'your-secret-key'

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

config = get_config()

HOST = config["MAIN"]["HOST"]
PORT = int(config["MAIN"]["PORT"])
DB_PATH = config["MAIN"]["DB_PATH"]
TIMEOUT = int(config["MAIN"]["TIMEOUT"])

# Set the directory to serve files from
FILES_PATH = 'resources'

#engine = create_engine(DB_PATH, 
#                       connect_args={"check_same_thread": False}, 
#                       poolclass=StaticPool)
#Base.metadata.create_all(engine)
#session_factory = sessionmaker(bind=engine)
#Session = scoped_session(session_factory)

#message_received_event = Event()
received_messages = {}
events_by_sid = {}

# The server runs locally and serves a single client at a time
sid = None


def check_auth(token=None):
    if token is None:
        return False
    # Validate token from the database
    session = Session()
    with session.begin():
        token_record = session.query(Token).filter(Token.token == token).first()

    if token_record is None:
        return False
    return True
    

@app.route('/resources/<path:path>')
def serve_files(path):
    return send_from_directory(FILES_PATH, path)


@app.route('/gpt/send_message', methods=['POST'])
def send_message():
    assert sid is not None, "No client connected"

    message = request.form.get('message')
    token = request.form.get('token')
    #if not check_auth(token):
    #    return 'Unauthorized', 401

    socketio.emit('message', message)

    event = Event()
    events_by_sid[sid] = event

    try:
        with Timeout(TIMEOUT):  
            event.wait()
            received_message = received_messages.pop(sid, 'Error: No message received')
            event.clear()
            return received_message
    except Timeout:
        return 'Error: Timeout occurred while waiting for a response'


@socketio.on('connect')
def handle_connect():
    token = request.args.get('token')
    #if not check_auth(token):
    #    return 'Unauthorized', 401
    global sid
    sid = request.sid
    print('Client connected:', request.sid)


@socketio.on('disconnect')
def handle_disconnect():
    global sid
    sid = None
    print('Client disconnected:', request.sid)


@socketio.on('message')
def handle_message(txt):
    print('received message: ' + txt)
    received_messages[request.sid] = txt
    event = events_by_sid.get(request.sid)
    if event:
        event.set()


if __name__ == '__main__':
    print(f"Starting server at address: {HOST}:{PORT}")
    socketio.run(app, host=HOST, port=PORT)
