DENIK

6.2.	 hw problem vse odpojeno. znovu propájeno, ok
7.2.	 nedůsledná analýza sk a usb karet, zmatek
8.2.	 udelalo se mi zle
9.2.	 zmizení meteostanice.py, nevím jak

11.2.	calcurse

┌───────────────────────────────┐
│          Calendar             │
│                               │
│  ← ↑ ↓ →  = pohyb kurzoru    │
│  n/p     = další/předchozí den │
│  N/P     = další/předchozí měsíc │
│  TAB     = přepínání panelů  │
└───────────────────────────────┘
            ↓
┌───────────────────────────────┐
│          Events Panel         │
│                               │
│  a       = přidat událost    │
│  e       = upravit            │
│  d       = smazat             │
│  ESC     = zrušit / opustit  │
│  TAB     = přepnutí panelů    │
└───────────────────────────────┘
            ↓
┌───────────────────────────────┐
│          TODO Panel           │
│                               │
│  t       = přidat úkol        │
│  e       = upravit úkol        │
│  d       = smazat úkol         │
│  ESC     = zrušit / opustit   │
│  TAB     = přepnutí panelů     │
└───────────────────────────────┘

───────────────────────────────

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

vypnutí myši v terminalu

printf '\e[?1000l'
printf '\e[?1002l'
printf '\e[?1006l'
nebo 
reset

MC
mc --nosubshell # když se není možno připojit pomocí SFTP



