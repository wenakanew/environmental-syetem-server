# EnviroMonitor Backend

A lightweight Flask backend for real-time air quality monitoring. It accepts sensor readings, performs anomaly classification, stores data in Firebase Realtime Database, and exposes REST endpoints consumed by the React dashboard.

Frontend repository: [environmental-system--dashboard](https://github.com/wenakanew/environmental-system--dashboard.git)

## Features
- Receive sensor data via HTTP (`POST /send`)
- Threshold-based anomaly classification
- Persist readings to Firebase Realtime Database
- Serve latest and recent readings to the frontend
- CORS enabled for local Vite dev server
- Simple sensor simulator for local testing

## Tech Stack
- Python, Flask, flask-cors
- Firebase Admin SDK (Realtime Database)

## Project Structure
```
backend/
├─ main.py                      # Flask app, routes
├─ anomaly_detection.py         # Simple threshold-based classifier
├─ utils/
│  ├─ firebase_helper.py        # Firebase init + read/write helpers
│  └─ sensor_simulator.py       # Random value simulator (posts to /send)
├─ firebase_config.json         # Service account (keep secret!)
├─ requirements.txt
└─ README.md
```

## Prerequisites
- Python 3.10+
- Firebase project with Realtime Database enabled
- A Firebase service account key JSON downloaded as `firebase_config.json` in the backend root

## Installation
```bash
# From backend directory
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt
```

## Firebase Setup
1. In Firebase Console, enable Realtime Database (in test mode for local dev, or add rules for prod).
2. Create a Service Account key (Project Settings → Service accounts → Generate new private key) and save it as `firebase_config.json` in this directory.
3. Confirm the database URL in `utils/firebase_helper.py` matches your project:
   - `https://<your-project-id>-default-rtdb.firebaseio.com/`

Database paths used:
- `sensor_readings/` — stores readings pushed by the backend

## Running the Backend
```bash
python main.py
# Service listens on http://0.0.0.0:5000
```

CORS is enabled for:
- `http://localhost:5173`
- `http://127.0.0.1:5173`
- `*` (for development)

## Endpoints
- `GET /health` → Service heartbeat
- `POST /send` → Accept a new sensor reading
- `GET /readings/latest` → Latest reading object or `null`
- `GET /readings?limit=20` → Array of recent readings (sorted ascending by time)

### Request/Response Details

#### POST /send
Request body:
```json
{ "air_quality": 123.45 }
```
Processing:
- Classifies `air_quality` into `status` and `message`
- Adds ISO `timestamp`
- Persists to `sensor_readings/` in Firebase

Response (200):
```json
{
  "success": true,
  "data": {
    "air_quality": 123.45,
    "timestamp": "2025-11-04T10:15:00.000Z",
    "status": "Unhealthy",
    "message": "Air quality degrading"
  }
}
```

#### GET /readings/latest
Returns a single reading object (or `null`). Example:
```json
{
  "air_quality": 123,
  "status": "Unhealthy",
  "timestamp": "2025-11-04T10:15:00Z"
}
```

#### GET /readings?limit=20
Returns an array of readings (ascending by time). Example:
```json
[
  { "air_quality": 120, "status": "Moderate", "timestamp": "2025-11-04T10:05:00Z" },
  { "air_quality": 130, "status": "Unhealthy", "timestamp": "2025-11-04T10:10:00Z" }
]
```

## Frontend Integration
When the frontend sets `VITE_BACKEND_URL`, it uses the backend for current and recent readings and still reads anomalies from Firebase.
- Base URL: `http://localhost:5000`
- Polling (frontend):
  - `GET /readings/latest` every 5s
  - `GET /readings?limit=20` every 10s
- Mapping logic on the frontend accepts:
  - `value` or `air_quality`
  - `timestamp` as ISO string or number (ms)
  - optional `status` (derives if missing)

Frontend repo: [environmental-system--dashboard](https://github.com/wenakanew/environmental-system--dashboard.git)

## Sensor Simulator (optional)
Sends random values to the backend every 5 seconds.
```bash
python utils/sensor_simulator.py
```

## Curl Examples
```bash
# Health
curl http://localhost:5000/health

# Send a reading
curl -X POST http://localhost:5000/send \
  -H "content-type: application/json" \
  -d "{\"air_quality\": 98}"

# Latest
curl http://localhost:5000/readings/latest

# Last 20
curl "http://localhost:5000/readings?limit=20"
```

## Anomaly Classification
See `anomaly_detection.py` for a simple rule-based approach:
- `< 50` → Good
- `50–99` → Moderate
- `100–199` → Unhealthy
- `≥ 200` → Hazardous

You can replace this with a model later; keep the output fields `status` and `message` to preserve API compatibility.

## Configuration Notes
- The backend expects `firebase_config.json` in the project root.
- Update the `databaseURL` in `utils/firebase_helper.py` to your Firebase URL.
- CORS origins are configured in `main.py`.

## Deployment
- Bind the Flask server behind a production WSGI (e.g., gunicorn) or containerize.
- Configure environment variables/secrets to supply the Firebase service account securely.
- Restrict CORS origins to your production frontend domain.

## Troubleshooting
- 401/permission errors: verify Realtime Database rules and service account permissions.
- Empty responses:
  - Ensure data exists under `sensor_readings/`.
  - Check timestamps are correctly written.
- CORS errors: confirm frontend origin is allowed in `main.py` CORS config.
- Connection issues: verify the backend runs on `http://localhost:5000` and no firewalls block requests.

## License
This backend is provided as-is for the EnviroMonitor project.





