from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import datetime
import os

app = Flask(__name__)

# ---------------------------------------------
# Allow frontend access
# ---------------------------------------------
CORS(app, resources={r"/*": {"origins": "*"}})

# ---------------------------------------------
# Firebase Initialization
# ---------------------------------------------
cred = credentials.Certificate("firebase-key.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://smart-environmental-syst-ff8bb-default-rtdb.firebaseio.com/"
})

# Reference to RTDB path
ref = db.reference("/sensor_readings")


# ---------------------------------------------
# ROUTES
# ---------------------------------------------

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "ok": True,
        "service": "backend",
        "time": datetime.datetime.now().isoformat(),
        "endpoints": {
            "send": "POST /send",
            "readings": "GET /readings?limit=100",
            "latest": "GET /readings/latest",
            "health": "GET /health"
        }
    }), 200


@app.route('/send', methods=['POST'])
def receive_data():
    try:
        data = request.get_json(force=True)
        print("Received data:", data)

        # Extract sensor values
        air_quality = float(data.get("air_quality", 0))

        # Timestamp
        timestamp = datetime.datetime.now().isoformat()

        # Create clean payload
        payload = {
            "air_quality": air_quality,
            "timestamp": timestamp
        }

        # Push directly to Firebase RTDB
        ref.push(payload)

        print("Uploaded to Firebase:", payload)

        return jsonify({"success": True, "uploaded": payload}), 200

    except Exception as e:
        print("Error in /send:", e)
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/readings', methods=['GET'])
def get_readings():
    try:
        limit = int(request.args.get("limit", 100))

        data = ref.order_by_key().limit_to_last(limit).get()
        if not data:
            return jsonify([]), 200

        # Convert dict -> list
        readings = list(data.values())

        return jsonify(readings), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/readings/latest', methods=['GET'])
def latest_reading():
    try:
        data = ref.order_by_key().limit_to_last(1).get()
        if not data:
            return jsonify(None), 200

        latest = list(data.values())[0]
        return jsonify(latest), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "ok": True,
        "service": "backend",
        "time": datetime.datetime.now().isoformat()
    }), 200


# ---------------------------------------------
# Render Production Server
# ---------------------------------------------
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

