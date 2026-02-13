from astral import LocationInfo
from astral.sun import sun
from astral.moon import moonrise, moonset, phase
from datetime import date
import csv

# ====== NASTAV SI POLOHU ======
LAT = 50.1
LON = 14.4
TZ  = "Europe/Prague"

city = LocationInfo("Home", "CZ", TZ, LAT, LON)
today = date.today()

# Slunce
s = sun(city.observer, date=today)
sunrise = s["sunrise"]
sunset = s["sunset"]
day_length = sunset - sunrise

# Měsíc
mr = moonrise(city.observer, date=today)
ms = moonset(city.observer, date=today)
moon_phase_val = phase(today)

# Převod fáze na text
def phase_name(p):
    if p < 1 or p > 28:
        return "Nov"
    elif p < 7:
        return "Dorůstající srpek"
    elif p < 9:
        return "První čtvrť"
    elif p < 14:
        return "Dorůstající Měsíc"
    elif p < 16:
        return "Úplněk"
    elif p < 22:
        return "Couvající Měsíc"
    elif p < 24:
        return "Poslední čtvrť"
    else:
        return "Ubývající srpek"

moon_phase_text = phase_name(moon_phase_val)

# Zápis do CSV
with open("/var/www/html/meteostanice/sun.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date","sunrise","sunset","day_length","moonrise","moonset","moon_phase"])
    writer.writerow([
        today,
        sunrise.strftime("%H:%M"),
        sunset.strftime("%H:%M"),
        str(day_length)[:5],
        mr.strftime("%H:%M") if mr else "",
        ms.strftime("%H:%M") if ms else "",
        moon_phase_text
    ])
