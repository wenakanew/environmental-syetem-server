from flask import Flask, request, jsonify
from utils.firebase_helper import send_data
from anomaly_detection import detect_anomaly
import datetime

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
