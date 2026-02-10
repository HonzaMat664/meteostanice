#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime
import os

DATA_DIR = "/var/www/html/meteostanice"
ALLOWED_STATIONS = {
    "station_1",
    "station_2",
    "station_3",
    "station_4"
}

API_KEY = "tajny-klic-123"   # změň si podle potřeby
os.makedirs(DATA_DIR, exist_ok=True)

class ReceiverHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # --- autentizace ---
        if self.headers.get("X-API-Key") != API_KEY:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Forbidden")
            return

        # --- načtení dat ---
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return

        # --- validace stanice ---
        station = data.get("station_id")
        if station not in ALLOWED_STATIONS:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Unknown station")
            return

        # --- extrakce a kontrola hodnot ---
        try:
            aht_temp = float(data["aht_temp"])
            aht_hum = float(data["aht_hum"])
            bmp_temp = float(data["bmp_temp"])
            pressure_hpa = float(data["pressure_hpa"])
        except (KeyError, ValueError):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid payload")
            return

        # --- generování timestamp ---
        timestamp = datetime.now().isoformat(timespec="seconds")

        # --- cesta k CSV ---
        csv_path = os.path.join(DATA_DIR, f"{station}.csv")

        # --- zápis do CSV ---
        new_file = not os.path.exists(csv_path)
        with open(csv_path, "a") as f:
            if new_file:
                f.write("timestamp,aht_temp,aht_hum,bmp_temp,pressure_hpa\n")
            f.write(f"{timestamp},{aht_temp},{aht_hum},{bmp_temp},{pressure_hpa}\n")

        # --- odpověď ---
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), ReceiverHandler)
    print("Receiver running on port 8080")
    server.serve_forever()
