from flask import Flask, jsonify
import requests
import random
import threading
import time
import os

app = Flask(__name__)

# Backend URL to send mock data to
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://127.0.0.1:5000')

# Track simulator status
simulator_status = {
    'running': False,
    'last_sent': None,
    'total_sent': 0,
    'errors': 0
}

def send_mock_data():
    """Continuously send mock sensor data to the backend"""
    print(f"Simulator started, sending data to {BACKEND_URL}/send")
    
    while True:
        try:
            value = random.uniform(30, 250)
            payload = {"air_quality": value}
            
            r = requests.post(f"{BACKEND_URL}/send", json=payload, timeout=10)
            
            simulator_status['last_sent'] = {
                'value': round(value, 2),
                'timestamp': time.time(),
                'response': r.json()
            }
            simulator_status['total_sent'] += 1
            
            print(f"Sent: {value:.2f} | Response: {r.json()}")
            
        except Exception as e:
            simulator_status['errors'] += 1
            print(f"Error: {e}")
        
        time.sleep(5)

@app.route('/', methods=['GET'])
def home():
    """Health check and status endpoint"""
    return jsonify({
        'service': 'Mock Sensor Simulator',
        'status': 'running',
        'backend_url': BACKEND_URL,
        'simulator': simulator_status
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Render"""
    return jsonify({'ok': True}), 200

@app.route('/status', methods=['GET'])
def status():
    """Get simulator status"""
    return jsonify(simulator_status), 200

# Start the simulator in a background thread when the app starts
def start_simulator():
    simulator_thread = threading.Thread(target=send_mock_data, daemon=True)
    simulator_thread.start()
    simulator_status['running'] = True

# Start simulator when app initializes
start_simulator()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)

