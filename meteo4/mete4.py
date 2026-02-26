import os
import glob
import csv
import time
import subprocess

# ====== SOUBOR CSV A CÍLOVÝ HOST ======
csv_file = "/home/honza/data4.csv"
remote_host = "192.168.1.159"
remote_path = "/home/honza/nas-web/data4.csv"
remote_user = "honza"
data4_path = "/home/honza/data4.py"

# ====== FUNKCE PRO ČTENÍ DS18B20 ======
def read_all_ds18b20():
    base_dir = '/sys/bus/w1/devices/'
    sensors = glob.glob(base_dir + '28*')
    temps = {}
    for sensor in sensors:
        sensor_id = os.path.basename(sensor)
        device_file = sensor + '/w1_slave'
        with open(device_file, 'r') as f:
            lines = f.readlines()
        # kontrola CRC
        if lines[0].strip()[-3:] != 'YES':
            temps[sensor_id] = None
            continue
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temps[sensor_id] = round(temp_c, 2)
        else:
            temps[sensor_id] = None
    return temps

# ====== VYTVOŘENÍ data4.py ======
def write_data_py(temps):
    dir_path = os.path.dirname(data4_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(data4_path, "w") as f:
        f.write("# Auto-generated file\n")
        for sensor_id, temp in temps.items():
            f.write(f"{sensor_id.replace('-', '_')} = {temp}\n")

# ====== ZÁPIS DO CSV ======
def zapis_do_csv(temps):
    from datetime import datetime
    now = datetime.now()
    datum = now.strftime("%Y-%m-%d")
    cas = now.strftime("%H:%M:%S")

    # Hlavička pokud soubor neexistuje
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            header = ["Datum","Cas"] + list(temps.keys())
            writer.writerow(header)

    # Zápis dat
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        row = [datum, cas] + list(temps.values())
        writer.writerow(row)

# ====== POSLÁNÍ CSV přes SCP ======
def send_csv():
    subprocess.run([
        "scp",
        csv_file,
        f"{remote_user}@{remote_host}:{remote_path}"
    ])

# ====== Hlavní smyčka ======
if __name__ == "__main__":
    while True:
        temps = read_all_ds18b20()
        for sensor, temp in temps.items():
            print(sensor, ":", temp, "°C")
        write_data_py(temps)
        zapis_do_csv(temps)
        send_csv()
        print("CSV posláno na", remote_host)
        time.sleep(60)  # čeká 60 sekund mezi zápisy
