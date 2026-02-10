import requests

MASTER_URL = "http://192.168.1.157:8080"  # ← sem dosadíš IP mastera
API_KEY = "tajny-klic-123"

payload = {
    "station_id": "station_2",
    "aht_temp": 22.3,
    "aht_hum": 48.5,
    "bmp_temp": 21.9,
    "pressure_hpa": 1012.7
}

headers = {"X-API-Key": API_KEY}

r = requests.post(MASTER_URL, json=payload, headers=headers, timeout=5)
print(r.status_code, r.text)
