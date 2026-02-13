#!/bin/bash
# Meteostanice – update dat a push na GitHub
# ----------------------------------------

set -e  # pokud některý příkaz selže, skript okamžitě skončí

LOGFILE="$HOME/update-data.log"
REPO_DIR="$HOME/nas-web"
CSV_DIR="/var/www/html/meteostanice"
FILES_TO_COPY=("data.csv" "pressure_correction.csv" "data_station2.csv" "sun.csv")

echo "=== $(date) – Update start ===" >> "$LOGFILE"

cd "$HOME/meteostaniceGIT"

# 1️⃣ Vygeneruj hlavní data meteostanice
echo "Generating meteostation data..." >> "$LOGFILE"
$HOME/meteo-venv/bin/python meteostanice.py >> "$LOGFILE" 2>&1

# 2️⃣ Vygeneruj Sun/Moon data do sun.csv
echo "Generating sun/moon data..." >> "$LOGFILE"
$HOME/meteo-venv/bin/python sun.py >> "$LOGFILE" 2>&1

# 3️⃣ Zkopíruj CSV soubory do repozitáře
for file in "${FILES_TO_COPY[@]}"; do
    if [ -f "$CSV_DIR/$file" ]; then
        cp "$CSV_DIR/$file" "$REPO_DIR/"
        echo "Copied $file to repo" >> "$LOGFILE"
    else
        echo "Warning: $file not found in $CSV_DIR" >> "$LOGFILE"
    fi
done

# 4️⃣ Commit a push
cd "$REPO_DIR"
git add *.csv web/*
git commit -m "Update data $(date '+%Y-%m-%d %H:%M')" >> "$LOGFILE" 2>&1 || echo "No changes to commit" >> "$LOGFILE"
git push >> "$LOGFILE" 2>&1

echo "=== $(date) – Update finished ===" >> "$LOGFILE"
