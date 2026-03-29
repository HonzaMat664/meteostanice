#!/bin/bash
DATE=$(date +%Y-%m-%d_%H-%M-%S)
DEST_DIR="/mnt/nas/snapshots/$DATE"
LOGFILE="$HOME/snapshot.log"
mkdir -p "$DEST_DIR"

if mountpoint -q /mnt/nas; then

    # Projekty rsync
    rsync -rLD --delete ~/nas-web/ "$DEST_DIR/nas-web/"
    rsync -rLD --delete ~/meteostanice/ "$DEST_DIR/meteostanice/"

    # Systémové soubory tar (symlinky zachovány)
    tar czf "$DEST_DIR/fstab.tar.gz" /etc/fstab
    tar czf "$DEST_DIR/systemd-system.tar.gz" -C /etc systemd/system

    echo "$(date +'%Y-%m-%d %H:%M:%S') - Snapshot dokončen v $DEST_DIR" >> "$LOGFILE"
else
    echo "$(date +'%Y-%m-%d %H:%M:%S') - NAS není připojený, snapshot se nekoná!" >> "$LOGFILE"
fi
# ponechat jen 2 nejnovější snapshoty
ls -dt /mnt/nas/snapshots/* | tail -n +3 | xargs rm -rf
