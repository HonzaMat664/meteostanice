# test změny pro Git
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import csv
from pathlib import Path
import traceback
import systemd.daemon
import requests

# knihovny pro senzory
import board
import busio
import adafruit_ahtx0
import adafruit_bmp280

# ------------------------
# Watchdog
# ------------------------
WATCHDOG_INTERVAL = 10
last_watchdog = 0

def feed_watchdog():
    global last_watchdog
    now = time.monotonic()
    if now - last_watchdog >= WATCHDOG_INTERVAL:
        systemd.daemon.notify('WATCHDOG=1')
        last_watchdog = now

# ------------------------
# Nastavení
# ------------------------
DATA_FILE = "/var/www/html/meteostanice/data2.csv"
CORRECTION_FILE = "/var/www/html/meteostanice/pressure_correction2.csv"

SLEEP_SECONDS = 600
STATION_ALTITUDE = 350  # m

# fallback korekce, když Chotusice nefunguje
REFERENCE_FALLBACK_OFFSET = 0.1  # hPa

# URL s referenčním tlakem (Chotusice)
CHOTUSICE_URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=49.95&lon=15.38"

# ------------------------
# Inicializace senzorů
# ------------------------
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    aht20 = adafruit_ahtx0.AHTx0(i2c)
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
except Exception as e:
    systemd.daemon.notify('STATUS=Chyba při inicializaci senzorů')
    raise RuntimeError(e)

# ------------------------
# Funkce
# ------------------------
def pressure_to_sea_level(p_hpa, altitude_m):
    """Přepočet tlaku na hladinu moře"""
    return round(p_hpa / (1 - altitude_m / 44330) ** 5.255, 2)

def get_chotusice_pressure():
    """Načte referenční tlak Chotusice (hPa)"""
    try:
        r = requests.get(CHOTUSICE_URL, timeout=10)
        r.raise_for_status()
        data = r.json()
        return float(
            data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_pressure_at_sea_level"]
        )
    except Exception:
        return None

def log_error(e):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print(ts, "Chyba:", e)
    print(traceback.format_exc())
    systemd.daemon.notify(f"STATUS=Chyba: {e}")

# ------------------------
# CSV soubory
# ------------------------
Path(DATA_FILE).parent.mkdir(parents=True, exist_ok=True)

# data.csv (struktura beze změny)
if not Path(DATA_FILE).exists():
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(
            ["timestamp", "aht_temp", "aht_hum", "bmp_temp", "pressure_hpa"]
        )

# pressure_correction.csv (diagnostika + nový sloupec correction_source)
if not Path(CORRECTION_FILE).exists():
    with open(CORRECTION_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(
            [
                "timestamp",
                "bmp_raw_hpa",
                "pressure_msl_calc",
                "pressure_ref_chotusice",
                "correction_hpa",
                "pressure_final_hpa",
                "correction_source",
            ]
        )

# ------------------------
# Hlavní smyčka
# ------------------------
systemd.daemon.notify("READY=1")
print("Meteostanice spuštěna")

while True:
    try:
        feed_watchdog()

        ts = time.strftime("%Y-%m-%d %H:%M:%S")

        # měření
        aht_temp = round(aht20.temperature, 2)
        aht_hum = round(aht20.relative_humidity, 1)
        bmp_temp = round(bmp280.temperature, 2)
        bmp_raw = round(bmp280.pressure, 2)

        # přepočet na hladinu moře
        p_msl = pressure_to_sea_level(bmp_raw, STATION_ALTITUDE)

        # reference
        p_ref = get_chotusice_pressure()

        if p_ref is not None:
            correction = round(p_ref - p_msl, 2)
            correction_source = "CHOTUSICE"
        else:
            correction = REFERENCE_FALLBACK_OFFSET
            correction_source = "FALLBACK"

        p_final = round(p_msl + correction, 1)

        # --- data.csv (finální tlak, struktura beze změny)
        with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(
                [ts, aht_temp, aht_hum, bmp_temp, p_final]
            )

        # --- pressure_correction.csv (diagnostika + nový sloupec)
        with open(CORRECTION_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(
                [ts, bmp_raw, p_msl, p_ref, correction, p_final, correction_source]
            )

        # status pro systemd a tisk
        status = (
            f"{ts} | RAW {bmp_raw} hPa | MSL {p_msl} hPa | "
            f"REF {p_ref} | CORR {correction} ({correction_source}) | FINAL {p_final}"
        )
        print(status)
        systemd.daemon.notify(f"STATUS={status}")

        for _ in range(SLEEP_SECONDS):
            feed_watchdog()
            time.sleep(1)

    except Exception as e:
        log_error(e)
        time.sleep(10)
