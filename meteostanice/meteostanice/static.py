#!/usr/bin/env python3
import ephem
import json
from datetime import datetime
from zoneinfo import ZoneInfo

# ==========================
# NASTAVENÍ POZOROVATELE
# ==========================
obs = ephem.Observer()
obs.lat = '49.8922106'
obs.lon = '15.5592397'
obs.elev = 350
obs.date = datetime.utcnow()  # UTC

# ==========================
# Slunce
# ==========================
sun = ephem.Sun()
sun_rise = obs.next_rising(sun)
sun_set = obs.next_setting(sun)
sun_noon = obs.next_transit(sun)

# ==========================
# Měsíc
# ==========================
moon = ephem.Moon()
moon_rise = obs.next_rising(moon)
moon_set = obs.next_setting(moon)
moon_phase = moon.phase

# ==========================
# FUNKCE PRO PŘEVOD NA CE(S)T
# ==========================
def to_local(ephem_date):
    dt_utc = ephem_date.datetime()  # datetime v UTC
    return dt_utc.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Europe/Prague"))

def fmt(dt):
    return dt.strftime("%Y-%m-%d %H:%M")

# ==========================
# VYTVOŘÍME JSON
# ==========================
data = {
    "generated": fmt(datetime.now(ZoneInfo("Europe/Prague"))),

    "sun": {
        "rise": fmt(to_local(sun_rise)),
        "set": fmt(to_local(sun_set)),
        "noon": fmt(to_local(sun_noon))
    },

    "moon": {
        "rise": fmt(to_local(moon_rise)),
        "set": fmt(to_local(moon_set)),
        "phase": round(moon_phase, 2)
    }
}

# ==========================
# ULOŽENÍ
# ==========================
with open("/home/honza/nas-web/data/static.json", "w") as f:
    json.dump(data, f, indent=2)
