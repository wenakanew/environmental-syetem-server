import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase app once with the correct Realtime Database URL
cred = credentials.Certificate("firebase_config.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smart-environmental-syst-ff8bb-default-rtdb.firebaseio.com/'
    })

SENSOR_READINGS_PATH = 'sensor_readings'

def send_data(sensor_data):
    # Write to /sensor_readings with the full payload (including status, message, timestamp)
    ref = db.reference(SENSOR_READINGS_PATH)
    ref.push(sensor_data)

def get_recent_readings(limit=100):
    ref = db.reference(SENSOR_READINGS_PATH)
    # Firebase RTDB doesn't support order+limit without an index; order by timestamp string
    snapshot = ref.order_by_child('timestamp').limit_to_last(int(limit)).get()
    if not snapshot:
        return []
    # snapshot is a dict of {key: value}; return list sorted by timestamp ascending
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