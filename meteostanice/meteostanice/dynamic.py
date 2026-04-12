import json
import ephem
from datetime import datetime, timedelta, timezone

# =========================
# CONFIG
# =========================
JSON_FILE = "/home/honza/nas-web/data/dynamic_24h.json"

# =========================
# OBSERVER (doplň si svoje)
# =========================
obs = ephem.Observer()
obs.lat = '49.8922106'
obs.lon = '16.2829961'
obs.elevation = 400
obs.pressure = 0

# =========================
# STABILNÍ ANCHOR (KLÍČ FIXU)
# =========================
now = datetime.now(timezone.utc)

# vždy pevná půlnoc UTC
start = datetime(
    now.year,
    now.month,
    now.day,
    tzinfo=timezone.utc
)

measurements = []

# =========================
# VÝPOČET 24H (144 bodů po 10 min)
# =========================
for i in range(0, 24 * 6):
    current_time = start + timedelta(minutes=10 * i)

    obs.date = current_time

    sun = ephem.Sun()
    moon = ephem.Moon()
    venus = ephem.Venus()
    mars = ephem.Mars()
    jupiter = ephem.Jupiter()

    sun.compute(obs)
    moon.compute(obs)
    venus.compute(obs)
    mars.compute(obs)
    jupiter.compute(obs)

    measurements.append({
        "timestamp": current_time.isoformat(),

        "sun_az": round(sun.az * 180 / ephem.pi, 2),
        "sun_alt": round(sun.alt * 180 / ephem.pi, 2),

        "moon_az": round(moon.az * 180 / ephem.pi, 2),
        "moon_alt": round(moon.alt * 180 / ephem.pi, 2),

        "venus_az": round(venus.az * 180 / ephem.pi, 2),
        "venus_alt": round(venus.alt * 180 / ephem.pi, 2),

        "mars_az": round(mars.az * 180 / ephem.pi, 2),
        "mars_alt": round(mars.alt * 180 / ephem.pi, 2),

        "jupiter_az": round(jupiter.az * 180 / ephem.pi, 2),
        "jupiter_alt": round(jupiter.alt * 180 / ephem.pi, 2),
    })

# =========================
# ULOŽENÍ (STRUKTURA ZACHOVÁNA)
# =========================
with open(JSON_FILE, "w") as f:
    json.dump({"measurements": measurements}, f, indent=2)
