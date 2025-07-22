from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

premium_keys = ["demo123", "goldkey", "testkey"]

@app.route('/validate-premium', methods=['POST'])
def validate_key():
    data = request.json
    if data['premiumKey'] in premium_keys:
        return jsonify({'isPremium': True, 'message': 'Valid key'})
    return jsonify({'isPremium': False, 'message': 'Invalid Key'})

@app.route('/check', methods=['POST'])
def check_numbers():
    data = request.json
    numbers = data.get('numbers', [])
    session_id = data.get('sessionId', '')
    
    registered = []
    not_registered = []

    total = len(numbers)
    for i, number in enumerate(numbers):
        time.sleep(0.5)  # simulate delay
        if number.endswith("0") or number.endswith("5"):
            registered.append(number)
        else:
            not_registered.append(number)

        socketio.emit('progress', {
            'type': 'progress',
            'currentProgress': i + 1,
            'totalNumbers': total
        }, to=session_id)

    return jsonify({
        'registered': registered,
        'notRegistered': not_registered,
        'totalNumbers': total
    })

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10000)
