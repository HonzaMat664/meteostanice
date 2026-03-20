#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import datetime
import ephem
import pytz
import signal
import math

# ==========================
# TIMEOUT ochrana (30 s max)
# ==========================
def timeout_handler(signum, frame):
    raise TimeoutError("Script timeout")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)

# ==========================
# Konstanty
# ==========================
LAT = '49.8922106'
LON = '15.5592397'
TZ = "Europe/Prague"

# ==========================
# Čas
# ==========================
tz = pytz.timezone(TZ)
now_local = datetime.datetime.now(tz)
now_utc = now_local.astimezone(pytz.utc)

# NOVÝ ISO FORMÁT
casovy_razitko = now_local.strftime("%Y-%m-%d %H:%M:%S")

# ==========================
# CSV adresář
# ==========================
csv_dir = "/home/honza/nas-web/data"
os.makedirs(csv_dir, exist_ok=True)
csv_file = os.path.join(csv_dir, "vychod.csv")

# ==========================
# Observer
# ==========================
observer = ephem.Observer()
observer.lat = LAT
observer.lon = LON
observer.date = now_utc

# ==========================
# Slunce
# ==========================
sun = ephem.Sun(observer)
sunrise = ephem.localtime(observer.next_rising(sun))
sunset  = ephem.localtime(observer.next_setting(sun))

# ==========================
# Měsíc
# ==========================
moon = ephem.Moon(observer)

moonrise = ephem.localtime(observer.next_rising(moon))
moonset  = ephem.localtime(observer.next_setting(moon))

moon_alt = math.degrees(moon.alt)
moon_az  = math.degrees(moon.az)
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

# ==========================
# Přeformátování časů (ISO)
# ==========================
sunrise_str = sunrise.strftime("%Y-%m-%d %H:%M:%S")
sunset_str  = sunset.strftime("%Y-%m-%d %H:%M:%S")
moonrise_str = moonrise.strftime("%Y-%m-%d %H:%M:%S")
moonset_str  = moonset.strftime("%Y-%m-%d %H:%M:%S")
next_full_str = next_full.strftime("%Y-%m-%d %H:%M:%S")

# ==========================
# Debug print
# ==========================
print("=== DENNÍ DATA ===")
print("Čas zápisu:", casovy_razitko)
print("Slunce východ:", sunrise_str)
print("Slunce západ :", sunset_str)
print("Měsíc fáze   :", phase_text)
print("Osvětlení    :", phase, "%")
print("Nejbližší úplněk:", next_full_str)

# ==========================
# Zápis do CSV
# ==========================
header = [
    "Datum_cas",
    "Slunce_vychod", "Slunce_zapad",
    "Mesic_vychod", "Mesic_zapad",
    "Mesic_vyska", "Mesic_azimut",
    "Mesic_faze", "Mesic_osvetleni",
    "Nejblizsi_uplnek"
]

row = [
    casovy_razitko,
    sunrise_str, sunset_str,
    moonrise_str, moonset_str,
    round(moon_alt, 2), round(moon_az, 2),
    phase_text, phase,
    next_full_str
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
