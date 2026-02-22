#!/bin/bash
# upda.sh – automatická synchronizace data.csv s GitHub

# Přejít do adresáře repozitáře
cd /home/honza/nas-web || exit 1

# Přidat pouze data.csv
git add data.csv

# Commitnout změny (včetně prázdného commitu pokud se nic nezměnilo)
git commit -m "Automatická aktualizace CSV $(date '+%Y-%m-%d %H:%M:%S')" --allow-empty

# Pushnout na GitHub
git push origin main

echo "Synchronizace CSV dokončena $(date '+%Y-%m-%d %H:%M:%S')"
