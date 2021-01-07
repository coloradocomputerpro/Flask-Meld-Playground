import os
from flask import Flask, request, send_from_directory
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask_meld import Meld


meld = Meld()

global async_mode
global cors_allowed_origins

async_mode = None # None is best to allow SocketIO to automatically run the best condition
cors_allowed_origins = '*' # this needs to be set to your domain name for production, wildcard is only for development/test

thread = None
thread_lock = Lock()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskapp.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    socketio = SocketIO(app, async_mode=async_mode,
                        cors_allowed_origins=cors_allowed_origins)

    meld.init_app(app, socketio)

    def background_thread():
        """Example of how to send server generated events to clients."""
        count = 0
        while True:
            socketio.sleep(10)
            count += 1
            socketio.emit('my_response',
                          {'data': 'Server generated event', 'count': count})

    @app.route('/')
    def index():
        return render_template('base.html', async_mode=socketio.async_mode)

    @app.socketio.event
    def my_event(message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']})

    @app.socketio.event
    def my_broadcast_event(message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']},
             broadcast=True)

    @app.socketio.event
    def join(message):
        join_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'In rooms: ' + ', '.join(rooms()),
              'count': session['receive_count']})

    @app.socketio.event
    def leave(message):
        leave_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'In rooms: ' + ', '.join(rooms()),
              'count': session['receive_count']})

    @app.socketio.on('close_room')
    def on_close_room(message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                             'count': session['receive_count']},
             to=message['room'])
        close_room(message['room'])

    @app.socketio.event
    def my_room_event(message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']},
             to=message['room'])

    @app.socketio.event
    def disconnect_request():
        @copy_current_request_context
        def can_disconnect():
            disconnect()

        session['receive_count'] = session.get('receive_count', 0) + 1
        # for this emit we use a callback function
        # when the callback function is invoked we know that the message has been
        # received and it is safe to disconnect
        emit('my_response',
             {'data': 'Disconnected!', 'count': session['receive_count']},
             callback=can_disconnect)

    @app.socketio.event
    def my_ping():
        emit('my_pong')

    @app.socketio.event
    def connect():
        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(background_thread)
        emit('my_response', {'data': 'Connected', 'count': 0})

    @app.socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected', request.sid)

    return app
