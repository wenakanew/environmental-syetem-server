import firebase_admin
from firebase_admin import credentials, db

# Path to your Firebase service account JSON
SERVICE_ACCOUNT_PATH = "firebase_config.json"
DATABASE_URL = "https://smart-environmental-syst-ff8bb-default-rtdb.firebaseio.com/"

# Initialize Firebase app once
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': DATABASE_URL
    })

SENSOR_READINGS_PATH = 'sensor_readings'


def send_data(sensor_data):
    try:
        ref = db.reference(SENSOR_READINGS_PATH)
        ref.push(sensor_data)
        print("Data pushed to Firebase:", sensor_data)
    except Exception as e:
        print("Firebase push error:", e)


def get_recent_readings(limit=100):
    try:
        ref = db.reference(SENSOR_READINGS_PATH)
        snapshot = ref.order_by_child('timestamp').limit_to_last(int(limit)).get()
        if not snapshot:
            return []
        readings = list(snapshot.values())
        readings.sort(key=lambda r: r.get('timestamp', ''))
        return readings
    except Exception as e:
        print("Error fetching recent readings:", e)
        return []


def get_latest_reading():
    readings = get_recent_readings(limit=1)
    if readings:
        return readings[-1]
    return None

    return None
