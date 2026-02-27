#!/bin/bash
# update.sh – automatická synchronizace CSV s GitHub (oneshot)
# Umístění: /home/honza/meteostanice/update.sh

# Timeout (max 60 s) 
timeout 60s bash <<'EOF'

# Přejít do repozitáře
cd /home/honza/nas-web || exit 1

# Přidat CSV soubory
git add data.csv azimut.csv vychod.csv

# Commit (i prázdný)
git commit -m "Automatická aktualizace CSV $(date '+%Y-%m-%d %H:%M:%S')" --allow-empty

# Push na GitHub
git push origin main

echo "Synchronizace CSV dokončena $(date '+%Y-%m-%d %H:%M:%S')"

EOF
