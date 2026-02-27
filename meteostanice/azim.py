#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import datetime
import math
import ephem

LAT = '50.1'
LON = '14.4'

# ===== ČAS =====
# Ephem chce UTC
now_utc = datetime.datetime.utcnow()

# Lokální čas jen pro zápis do CSV
now_local = datetime.datetime.now()

csv_dir = os.path.expanduser("~/nas-web")
os.makedirs(csv_dir, exist_ok=True)

observer = ephem.Observer()
observer.lat = LAT
observer.lon = LON
observer.date = now_utc   # <-- přímo UTC bez pytz

# ===== SLUNCE =====
sun = ephem.Sun(observer)
sun_alt = math.degrees(sun.alt)
sun_az  = math.degrees(sun.az)

# ===== MĚSÍC =====
moon = ephem.Moon(observer)
moon_alt = math.degrees(moon.alt)
moon_az  = math.degrees(moon.az)

print("=== AKTUÁLNÍ POLOHA ===")
print("UTC čas:", now_utc.strftime("%H:%M:%S"))
print("Slunce:", round(sun_alt,2), "° /", round(sun_az,2), "°")
print("Měsíc :", round(moon_alt,2), "° /", round(moon_az,2), "°")

# ===== ZÁPIS DO azimut.csv =====
csv_file = os.path.join(csv_dir, "azimut.csv")

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

if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

with open(csv_file, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(row)
