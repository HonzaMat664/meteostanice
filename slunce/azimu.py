#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import datetime
import ephem
import pytz

LAT = '50.1'
LON = '14.4'
TZ = "Europe/Prague"

tz = pytz.timezone(TZ)
now_local = datetime.datetime.now(tz)

# ephem počítá v UTC
now_utc = now_local.astimezone(pytz.utc)

csv_dir = os.path.expanduser("~/nas-web")
os.makedirs(csv_dir, exist_ok=True)

observer = ephem.Observer()
observer.lat = LAT
observer.lon = LON
observer.date = now_utc

# ===== SLUNCE =====
sun = ephem.Sun(observer)
sun_alt = float(sun.alt) * 180 / 3.141592653589793
sun_az  = float(sun.az) * 180 / 3.141592653589793

# ===== MĚSÍC =====
moon = ephem.Moon(observer)
moon_alt = float(moon.alt) * 180 / 3.141592653589793
moon_az  = float(moon.az) * 180 / 3.141592653589793

print("=== AKTUÁLNÍ POLOHA ===")
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
