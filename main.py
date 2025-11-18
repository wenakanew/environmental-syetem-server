from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.firebase_helper import send_data, get_recent_readings, get_latest_reading
from anomaly_detection import detect_anomaly
import datetime

app = Flask(__name__)
# Enable CORS for local dashboards (5173, 8080)
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "*"
]}})

@app.route('/', methods=['GET'])
def root():
    try:
        latest = get_latest_reading()
        return jsonify({
            "ok": True,
            "service": "backend",
            "time": datetime.datetime.now().isoformat(),
            "latest": latest,
            "endpoints": {
                "send": "POST /send",
                "readings": "GET /readings?limit=100",
                "latest": "GET /readings/latest",
                "health": "GET /health"
            }
        }), 200
    except Exception as e:
        return jsonify({
            "ok": False,
            "service": "backend",
            "time": datetime.datetime.now().isoformat(),
            "error": str(e)
        }), 500

@app.route('/send', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        air_quality = float(data.get('air_quality', 0))
        timestamp = datetime.datetime.now().isoformat()

        # Run anomaly detection
        anomaly = detect_anomaly(air_quality)

        payload = {
            'air_quality': air_quality,
            'timestamp': timestamp,
            'status': anomaly['status'],
            'message': anomaly['message']
        }

        # Push to Firebase
        send_data(payload)

        return jsonify({"success": True, "data": payload}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/readings', methods=['GET'])
def get_readings():
    try:
        limit = int(request.args.get('limit', 100))
        readings = get_recent_readings(limit=limit)
        # Frontend expects a plain array
        return jsonify(readings), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/readings/latest', methods=['GET'])
def get_latest():
    try:
        latest = get_latest_reading()
        # Frontend expects a plain object (or null)
        return jsonify(latest), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"ok": True, "service": "backend", "time": datetime.datetime.now().isoformat()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
