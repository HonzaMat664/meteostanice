Meteostanice – přehled

Přehled skriptů a timerů

Skript	Funkce	Interval	CSV soubor	Systemd Service	Systemd Timer
measure.py	měření AHT20 + BMP280	5 min	data.csv + pressure_log.csv	meteomeasure.service	meteomeasure.timer
azimut.py	aktuální poloha Slunce a Měsíce	1 min	azimut.csv	azimut.service	azimut.timer
astro.py	denní východ/západ/fáze Měsíce	1× denně	vychod.csv	astro.service	astro.timer
update.sh	synchronizace CSV s GitHub	2–10 min	data.csv, azimut.csv, vychod.csv	update.service	update.timer

Poznámky
	•	Watchdog: doporučeno HW watchdog pro vzdálené stanice (restart při zamrznutí systému)
	•	TimeoutStartSec: ochrana proti zaseknutí skriptů (I2C, ephem, git)
	•	Persistent=true: po restartu RPi se spustí vynechané instance
	•	Testovací timer: lze změnit OnBootSec + OnUnitActiveSec pro rychlé ověření
	•	Logy: journalctl -u <service> -f
	•	CSV adresář: ~/nas-web – všechny skripty zapisují do CSV
	•	Umístění skriptů: /home/honza/meteostanice (kromě repozitáře ~/nas-web pro git)
	•	Odstranění starých služeb: zastavit, disable a smazat původní meteostanice.service a všechny staré upda služby/timery
