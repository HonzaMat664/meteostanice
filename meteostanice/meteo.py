#!/usr/bin/env python3

import time
import csv
import os
from datetime import datetime
import smbus
import struct

# ==========================
# KONSTANTY – uprav dle potřeby
# ==========================
CSV_FILE = "/home/honza/nas-web/data.csv"
CSV_PRESSURE_FILE = "/home/honza/pressure_log.csv"  # nový CSV pro tlak
INTERVAL = 300  # sekundy mezi měřeními
ALTITUDE_M = 350   # nadmořská výška stanice v metrech
OFFSET_HPA = -2.2   # korekční konstanta pro tlak

# ==========================
# I2C adresy čidel
# ==========================
AHT20_ADDR = 0x38
BMP280_ADDR = 0x77

bus = smbus.SMBus(1)

# ==========================
# Funkce pro AHT20
# ==========================
def read_aht20():
    try:
        bus.write_i2c_block_data(AHT20_ADDR, 0xAC, [0x33, 0x00])
        time.sleep(0.1)

        data = bus.read_i2c_block_data(AHT20_ADDR, 0x00, 6)

        humidity_raw = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4))
        temperature_raw = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5])

        humidity = humidity_raw * 100 / 1048576
        temperature = (temperature_raw * 200 / 1048576) - 50

        return round(temperature, 2), round(humidity, 2)

    except:
        return None, None

# ==========================
# Funkce pro BMP280
# ==========================
def read_bmp280_calibration():
    calib = bus.read_i2c_block_data(BMP280_ADDR, 0x88, 24)
    return struct.unpack('<HhhHhhhhhhhh', bytes(calib))

dig_T1, dig_T2, dig_T3, \
dig_P1, dig_P2, dig_P3, dig_P4, \
dig_P5, dig_P6, dig_P7, dig_P8, dig_P9 = read_bmp280_calibration()

t_fine = 0

def read_bmp280():
    global t_fine
    try:
        # Normal mode
        bus.write_byte_data(BMP280_ADDR, 0xF4, 0x27)
        bus.write_byte_data(BMP280_ADDR, 0xF5, 0xA0)
        time.sleep(0.1)

        data = bus.read_i2c_block_data(BMP280_ADDR, 0xF7, 6)
        adc_p = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        adc_t = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)

        # Temperature compensation
        var1 = (((adc_t >> 3) - (dig_T1 << 1)) * dig_T2) >> 11
        var2 = (((((adc_t >> 4) - dig_T1) * ((adc_t >> 4) - dig_T1)) >> 12) * dig_T3) >> 14
        t_fine = var1 + var2
        temperature = (t_fine * 5 + 128) >> 8
        temperature = temperature / 100.0

        # Pressure compensation
        var1 = t_fine - 128000
        var2 = var1 * var1 * dig_P6
        var2 = var2 + ((var1 * dig_P5) << 17)
        var2 = var2 + (dig_P4 << 35)
        var1 = ((var1 * var1 * dig_P3) >> 8) + ((var1 * dig_P2) << 12)
        var1 = (((1 << 47) + var1) * dig_P1) >> 33

        if var1 == 0:
            return None, None

        p = 1048576 - adc_p
        p = ((p << 31) - var2) * 3125 // var1
        var1 = (dig_P9 * (p >> 13) * (p >> 13)) >> 25
        var2 = (dig_P8 * p) >> 19
        pressure = ((p + var1 + var2) >> 8) + (dig_P7 << 4)
        pressure = pressure / 256.0 / 100.0  # hPa

        return round(temperature, 2), round(pressure, 2)

    except:
        return None, None

# ==========================
# Přepočet tlaku na hladinu moře
# ==========================
def sea_level_pressure(p, T, H=ALTITUDE_M, offset=OFFSET_HPA):
    if p is None or T is None:
        return None
    return round(p * (1 - (0.0065 * H) / (T + 0.0065 * H + 273.15)) ** -5.257 + offset, 2)

# ==========================
# CSV pro meteostanici
# ==========================
def write_csv(row):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "datetime",
                "temperature_C",
                "humidity_percent",
                "pressure_hPa",
                "pressure_sea_level_hPa"
            ])
        writer.writerow(row)

# ==========================
# CSV pro tlak + korekce
# ==========================
def write_pressure_csv(datetime_str, pressure, pressure_sl, offset=OFFSET_HPA):
    file_exists = os.path.isfile(CSV_PRESSURE_FILE)
    pressure_corrected = round(pressure_sl + offset, 2) if pressure_sl is not None else None
    with open(CSV_PRESSURE_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "datetime",
                "pressure_hPa",
                "pressure_sea_level_hPa",
                "pressure_corrected_hPa",
                "offset_hPa"
            ])
        writer.writerow([datetime_str, pressure, pressure_sl, pressure_corrected, offset])

# ==========================
# MAIN
# ==========================
def main():
    print("Meteostanice spuštěna")
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        temp_aht, humidity = read_aht20()
        temp_bmp, pressure = read_bmp280()

        pressure_sl = sea_level_pressure(pressure, temp_aht)

        # řádek pro hlavní CSV
        row = [now, temp_aht, humidity, pressure, pressure_sl]
        print(row)
        write_csv(row)

        # řádek pro CSV s tlakem a korekcí
        write_pressure_csv(now, pressure, pressure_sl)

        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
