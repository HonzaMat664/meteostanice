import ephem
import json
from datetime import datetime, timedelta
import math

# ===============================
# Nastavení pozorovatele
# ===============================
obs = ephem.Observer()
obs.lat = '49.8922106'
obs.lon = '15.5592397'
obs.elevation = 350

# začátek dne (UTC)
start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

# objekty
sun = ephem.Sun()
moon = ephem.Moon()

data = []

# ===============================
# Výpočet po 5 minutách (24h)
# ===============================
for i in range(0, 24 * 60, 5):
    t = start + timedelta(minutes=i)
    obs.date = t

    sun.compute(obs)
    moon.compute(obs)

    record = {
        "time": t.strftime("%H:%M"),
        "sun": {
            "alt": math.degrees(sun.alt),
            "az": math.degrees(sun.az)
        },
        "moon": {
            "alt": math.degrees(moon.alt),
            "az": math.degrees(moon.az),
            "phase": moon.phase
        }
    }

    data.append(record)

# ===============================
# Fáze Měsíce (globální info)
# ===============================
now = ephem.now()

output = {
    "meta": {
        "generated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "location": {
            "lat": obs.lat,
            "lon": obs.lon
        }
    },
    "moon_phases": {
        "next_full": str(ephem.next_full_moon(now)),
        "next_new": str(ephem.next_new_moon(now))
    },
    "data": data
}

# uložení
with open("/home/honza/nas-web/data/astro.json", "w") as f:
    json.dump(output, f, indent=2)
print("Vygenerováno: astro.json")
