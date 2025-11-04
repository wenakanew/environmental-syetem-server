def detect_anomaly(value):
    # Simple threshold-based detection (can be upgraded to ML model)
    if value < 50:
        return {"status": "Good", "message": "Air quality is safe"}
    elif 50 <= value < 100:
        return {"status": "Moderate", "message": "Slightly polluted"}
    elif 100 <= value < 200:
        return {"status": "Unhealthy", "message": "Air quality degrading"}
    else:
        return {"status": "Hazardous", "message": "Critical air pollution detected!"}
