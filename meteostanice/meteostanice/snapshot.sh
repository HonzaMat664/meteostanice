#!/bin/bash

DATE=$(date +%Y-%m-%d_%H-%M-%S)
SNAPDIR="/mnt/nas/snapshots"
TMP_DIR="$SNAPDIR/.tmp_$DATE"
FINAL_DIR="$SNAPDIR/$DATE"
LOGFILE="$HOME/snapshot.log"
LOCKFILE="/tmp/snapshot.lock"

# 🔒 LOCK – zabrání paralelnímu spuštění
if [ -f "$LOCKFILE" ]; then
    echo "$(date +'%Y-%m-%d %H:%M:%S') - Snapshot už běží, ukončuji." >> "$LOGFILE"
    exit 1
fi
trap "rm -f $LOCKFILE" EXIT
touch "$LOCKFILE"

# 🔍 kontrola mountu
if ! mountpoint -q /mnt/nas; then
    echo "$(date +'%Y-%m-%d %H:%M:%S') - NAS není připojený, snapshot se nekoná!" >> "$LOGFILE"
    exit 1
fi

mkdir -p "$TMP_DIR"

# 📁 Projekty rsync
rsync -rLD --delete --exclude="*.swp" --exclude="*.tmp" --exclude="*~" ~/nas-web/ "$TMP_DIR/nas-web/"
RSYNC1=$?

rsync -rLD --delete --exclude="*.swp" --exclude="*.tmp" --exclude="*~" ~/meteostanice/ "$TMP_DIR/meteostanice/"
RSYNC2=$?

# ⚙️ Systémové soubory
tar czf "$TMP_DIR/fstab.tar.gz" /etc/fstab
TAR1=$?

tar czf "$TMP_DIR/systemd-system.tar.gz" -C /etc systemd/system
TAR2=$?

# ✅ kontrola úspěšnosti
if [ $RSYNC1 -eq 0 ] && [ $RSYNC2 -eq 0 ] && [ $TAR1 -eq 0 ] && [ $TAR2 -eq 0 ]; then

    # 🔄 atomické přejmenování
    mv "$TMP_DIR" "$FINAL_DIR"

    echo "$(date +'%Y-%m-%d %H:%M:%S') - Snapshot OK: $FINAL_DIR" >> "$LOGFILE"

    # 🧹 mazání starých (ponechat 2)
    cd "$SNAPDIR" || exit
    ls -1dt */ | tail -n +3 | xargs -r rm -rf

else
    echo "$(date +'%Y-%m-%d %H:%M:%S') - Snapshot FAILED, nemažu nic!" >> "$LOGFILE"
    rm -rf "$TMP_DIR"
    exit 1
fi
