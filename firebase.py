import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-environmental-syst-ff8bb-default-rtdb.firebaseio.com'
})

def send_data(sensor_data):
    ref = db.reference('sensor_readings')
    ref.push(sensor_data)
