#!/bin/bash
# update-data.sh – automaticky commitne a pushne nové CSV do GitHubu
# Log: ~/update-data.log

LOGFILE="$HOME/update-data.log"
REPO_DIR="$HOME/nas-web"
CSV_DIR="/var/www/html/meteostanice"
FILES_TO_COPY=("data.csv" "pressure_correction.csv")

echo "$(date) | Spouštím update-data.sh" >> "$LOGFILE"

# přejdi do repozitáře
cd "$REPO_DIR" || { echo "$(date) | Chyba: Nelze přejít do $REPO_DIR" >> "$LOGFILE"; exit 1; }

# zkopíruj CSV soubory do repozitáře
for f in "${FILES_TO_COPY[@]}"; do
    if cp "$CSV_DIR/$f" "$REPO_DIR/"; then
        echo "$(date) | Zkopírován $f do repozitáře" >> "$LOGFILE"
    else
        echo "$(date) | Chyba: Nelze zkopírovat $f" >> "$LOGFILE"
    fi
done

# git add nové/změněné soubory
git add "${FILES_TO_COPY[@]}"

# commit pouze pokud jsou změny
if ! git diff --cached --quiet; then
    git commit -m "Auto-update CSV z meteostanice $(date '+%Y-%m-%d %H:%M:%S')"
    echo "$(date) | Commitnuty nové CSV" >> "$LOGFILE"
else
    echo "$(date) | Žádné změny k commitnutí" >> "$LOGFILE"
fi

# fetch + rebase z GitHubu
git fetch origin
if git rebase origin/main; then
    echo "$(date) | Rebase úspěšný" >> "$LOGFILE"
else
    echo "$(date) | Rebase narazil na konflikt – ručně vyřeš" >> "$LOGFILE"
    exit 1
fi

# push na GitHub
if git push origin main; then
    echo "$(date) | Push úspěšný" >> "$LOGFILE"
else
    echo "$(date) | Push selhal – zkontroluj token/SSH" >> "$LOGFILE"
    exit 1
fi

echo "$(date) | update-data.sh dokončen" >> "$LOGFILE"
