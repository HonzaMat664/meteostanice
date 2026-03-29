#!/bin/bash
# update.sh – automatická synchronizace CSV s GitHub (oneshot)

# Přesun do Git repozitáře
cd /home/honza/nas-web || exit 1

# Přidat všechny CSV změny v podsložce data
git add  -A

# Commit s timestampem (i prázdný commit)
git commit -m "Automatická aktualizace CSV $(date '+%Y-%m-%d %H:%M:%S')" --allow-empty

# Push na GitHub
git push origin main

echo "Synchronizace CSV dokončena $(date '+%Y-%m-%d %H:%M:%S')"
