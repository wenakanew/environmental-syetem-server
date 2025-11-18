import requests, random, time

while True:
    value = random.uniform(30, 250)
    payload = {"air_quality": value}
    r = requests.post("http://127.0.0.1:5000/send", json=payload)
    print(r.json())
    time.sleep(5)
