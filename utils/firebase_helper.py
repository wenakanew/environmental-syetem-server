import firebase_admin
from firebase_admin import credentials, db
import os

FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH", "firebase_config.json")

cred = credentials.Certificate(FIREBASE_CRED_PATH)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smart-environmental-syst-ff8bb-default-rtdb.firebaseio.com/'
    })

SENSOR_READINGS_PATH = 'sensor_readings'

def send_data(sensor_data):
    try:
        ref = db.reference(SENSOR_READINGS_PATH)
        ref.push(sensor_data)
        print("Firebase write successful:", sensor_data)
    except Exception as e:
        print("Firebase write failed:", e)

def get_recent_readings(limit=100):
    ref = db.reference(SENSOR_READINGS_PATH)
    snapshot = ref.order_by_child('timestamp').limit_to_last(int(limit)).get()
    if not snapshot:
        return []
    readings = list(snapshot.values())
    try:
        readings.sort(key=lambda r: r.get('timestamp', ''))
    except Exception:
        pass
    return readings

def get_latest_reading():
    readings = get_recent_readings(limit=1)
    if readings:
        return readings[-1]
    return None
