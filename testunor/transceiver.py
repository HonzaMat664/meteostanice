#!/usr/bin/env python3

import time
import requests

MASTER_URL = "http://192.168.1.157:8080"  # ← dosadit IP mastera
API_KEY = "tajny-klic-123"
STATION_ID = "station_2"
SEND_INTERVAL = 30  # sekundy mezi odesláním

# --- Funkce pro čtení senzorů ---
def read_sensors():
    """
    Nahraď následující řádky skutečným čtením ze senzorů
    AHT20 a BMP180/BMP280
    """
    aht_temp = 22.3       # °C z AHT20
    aht_hum = 48.5        # % z AHT20
    bmp_temp = 21.9       # °C z BMP
    pressure_hpa = 1012.7 # hPa z BMP
    return aht_temp, aht_hum, bmp_temp, pressure_hpa

# --- Odeslání dat na master ---
def send_data(aht_temp, aht_hum, bmp_temp, pressure_hpa):
    payload = {
        "station_id": STATION_ID,
        "aht_temp": aht_temp,
        "aht_hum": aht_hum,
        "bmp_temp": bmp_temp,
        "pressure_hpa": pressure_hpa
    }
    headers = {"X-API-Key": API_KEY}

    try:
        r = requests.post(MASTER_URL, json=payload, headers=headers, timeout=5)
        if r.status_code == 200:
            print(f"[OK] Data odeslána: {payload}")
        else:
            print(f"[WARN] Server vrátil status {r.status_code}")
    except requests.RequestException as e:
        print(f"[ERROR] Nepodařilo se odeslat data: {e}")

# --- Hlavní smyčka ---
def main():
    while True:
        aht_temp, aht_hum, bmp_temp, pressure_hpa = read_sensors()
        send_data(aht_temp, aht_hum, bmp_temp, pressure_hpa)
        time.sleep(SEND_INTERVAL)

if __name__ == "__main__":
    main()
