#!/usr/bin/env python3
import ephem
import json
from datetime import datetime, timedelta

# ==========================
# NASTAVENÍ POZOROVATELE
# ==========================
obs = ephem.Observer()
obs.lat = '49.8922106'      # zeměpisná šířka
obs.lon = '15.5592397'      # zeměpisná délka
obs.elevation = 350          # nadmořská výška (m)

# dnešní datum UTC (00:00)
today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

# interval v minutách
interval_min = 10
points_per_day = 24*60 // interval_min

data_list = []

# ==========================
# výpočet hodnot Měsíce pro celý den
# ==========================
for i in range(points_per_day):
    point_time = today + timedelta(minutes=i*interval_min)
    obs.date = point_time
    moon = ephem.Moon()
    moon.compute(obs)
    
    # základní údaje
    azimut = float(moon.az) * 180 / ephem.pi
    vyska = float(moon.alt) * 180 / ephem.pi
    ra = str(moon.ra)
    dec = str(moon.dec)
    vzdalenost_km = moon.earth_distance * 149597870.7  # AU → km
    uhlova_velikost = moon.size
    osvetleni = moon.phase  # procento osvětlení disku

    # stáří Měsíce od posledního novu
    previous_new_moon = ephem.previous_new_moon(obs.date)
    stari = obs.date - previous_new_moon

    # připrav bod
    data_list.append({
        "cas_utc": obs.date.datetime().isoformat(),
        "azimut_stupne": round(azimut, 2),
        "vyska_stupne": round(vyska, 2),
        "rektascenze": ra,
        "deklinace": dec,
        "vzdalenost_km": round(vzdalenost_km, 0),
        "uhlova_velikost_arcsec": uhlova_velikost,
        "osvetleni_procent": round(osvetleni, 2),
        "stari_dny": round(float(stari), 2)
    })

# ==========================
# uložit JSON
# ==========================
json_data = {
    "interval_min": interval_min,
    "data": data_list
}

output_file = "/home/honza/nas-web/data/mesic.json"
with open(output_file, "w") as f:
    json.dump(json_data, f, indent=4)

print(f"JSON pro celý den uložen: {output_file}, interval {interval_min} min, body: {len(data_list)}")
