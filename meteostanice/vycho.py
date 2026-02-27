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
now_utc = now_local.astimezone(pytz.utc)
today = now_local.date()

csv_dir = os.path.expanduser("~/nas-web")
os.makedirs(csv_dir, exist_ok=True)

observer = ephem.Observer()
observer.lat = LAT
observer.lon = LON
observer.date = now_utc

# ===== SLUNCE =====
sun = ephem.Sun(observer)
sunrise = ephem.localtime(observer.next_rising(sun))
sunset  = ephem.localtime(observer.next_setting(sun))

# ===== MĚSÍC =====
moon = ephem.Moon()

moonrise = ephem.localtime(observer.next_rising(moon))
moonset  = ephem.localtime(observer.next_setting(moon))

moon.compute(observer)
moon_alt = float(moon.alt) * 180 / 3.141592653589793
moon_az  = float(moon.az) * 180 / 3.141592653589793

phase = round(moon.phase, 1)

if phase < 1:
    phase_text = "Nov"
elif phase < 49:
    phase_text = "Dorůstá"
elif phase < 51:
    phase_text = "První čtvrť"
elif phase < 99:
    phase_text = "Couvá"
else:
    phase_text = "Úplněk"

next_full = ephem.localtime(ephem.next_full_moon(observer.date))

print("=== DENNÍ DATA ===")
print("Slunce východ:", sunrise)
print("Slunce západ :", sunset)
print("Měsíc fáze   :", phase_text)
print("Osvětlení    :", phase, "%")
print("Nejbližší úplněk:", next_full)

# ===== ZÁPIS DO vychod.csv =====
csv_file = os.path.join(csv_dir, "vychod.csv")

header = [
    "Datum",
    "Slunce_vychod", "Slunce_zapad",
    "Mesic_vychod", "Mesic_zapad",
    "Mesic_vyska", "Mesic_azimut",
    "Mesic_faze", "Mesic_osvetleni",
    "Nejblizsi_uplnek"
]

row = [
    today,
    sunrise, sunset,
    moonrise, moonset,
    round(moon_alt,2), round(moon_az,2),
    phase_text, phase,
    next_full
]

if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

with open(csv_file, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(row)
