změna IP adresy a GIT

sudo nano /etc/systemd/network/10-wlan0.network

obsah:
[Match]
Name=wlan0

[Network]
Address=192.168.1.156/24
Gateway=192.168.1.1
DNS=192.168.1.1

sudo systemctl enable systemd-networkd # důležité, aby i po restartu zůstala nově nastavená adresa

restart:
sudo systemctl restart systemd-networkd
hostname -I

156 testunor.  116
157 meteo.  101
158 meteo2 106
_________________________________________________
GIT

cd ~/meteostaniceGIT
git status
git add .
git commit -m "Zaloha po upravach z RPi2"
git push

struktura adresáře:
/home/honza/
├─ meteo-venv/              # virtualenv
├─ meteo-collector/
│   ├─ collector.py
│   └─ config.py            # IP, port, cesta k CSV
├─ update-data.sh
├─ meteostaniceGIT
└─ nas-web/                 # git repo (GitHub Pages)

branch?
