#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import datetime
import math
import ephem
import signal

# ==========================
# TIMEOUT ochrana (20 s max)
# ==========================
def timeout_handler(signum, frame):
    raise TimeoutError("Script timeout")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(20)

# ==========================
# Konstanty
# ==========================
LAT = '50.1'
LON = '14.4'

# ==========================
# Čas
# ==========================
now_utc = datetime.datetime.utcnow()
now_local = datetime.datetime.now()

# ==========================
# Vytvoření adresáře CSV
# ==========================
csv_dir = os.path.expanduser("~/nas-web")
os.makedirs(csv_dir, exist_ok=True)
csv_file = os.path.join(csv_dir, "azimut.csv")

# ==========================
# Pozorovatel
# ==========================
observer = ephem.Observer()
observer.lat = LAT
observer.lon = LON
observer.date = now_utc  # UTC

# ==========================
# Slunce
# ==========================
sun = ephem.Sun(observer)
sun_alt = math.degrees(sun.alt)
sun_az  = math.degrees(sun.az)

# ==========================
# Měsíc
# ==========================
moon = ephem.Moon(observer)
moon_alt = math.degrees(moon.alt)
moon_az  = math.degrees(moon.az)

# ==========================
# Debug print
# ==========================
print("=== AKTUÁLNÍ POLOHA ===")
print("UTC čas:", now_utc.strftime("%H:%M:%S"))
print("Slunce:", round(sun_alt,2), "° /", round(sun_az,2), "°")
print("Měsíc :", round(moon_alt,2), "° /", round(moon_az,2), "°")

# ==========================
# Zápis do CSV
# ==========================
header = [
    "Datum", "Cas",
    "Slunce_vyska", "Slunce_azimut",
    "Mesic_vyska", "Mesic_azimut"
]

row = [
    now_local.strftime("%Y-%m-%d"),
    now_local.strftime("%H:%M:%S"),
    round(sun_alt,2), round(sun_az,2),
    round(moon_alt,2), round(moon_az,2)
]

# Vytvoření CSV, pokud neexistuje
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

# Přidání řádku
with open(csv_file, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(row)

# ==========================
# Vypnutí timeoutu
# ==========================
signal.alarm(0)
