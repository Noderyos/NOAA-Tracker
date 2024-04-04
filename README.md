# NOAA Tracker

## Setup

### Run all commands as root

Setup database, create this table : 
```sql
CREATE TABLE pass(
   id DATETIME,
   satellite VARCHAR(50),
   duration INT,
   elevation INT,
   PRIMARY KEY(id)
);
```


```bash
# Install dependencies
sudo apt install rtl_sdr mariadb-server -y

# Secure mariadb install
mysql_secure_installation


# Retrieve project
git clone https://github.com/Noderyos/NOAA-Tracker /opt/NOAA

# Setup
cd /opt/NOAA
mkdir images
python3 -m venv venv
source venv/bin/activate
pip -r requirements.txt
```


### Install SatDump

Download last file `_arm64.deb` here : https://github.com/SatDump/SatDump/releases/latest with `wget https://github.com/SatDump/SatDump/releases/download/1.1.4/satdump_1.1.4_arm64.deb` (adapt with version name)

Install it by running `sudo apt install ./satdump_1.1.4_arm64.deb`


### Create website service

In `/etc/systemd/system/noaa_web.service`, put

```
[Unit]
Description=NOAA Capture images website
After=network.target

[Service]
Type=simple
Restart=always
WorkingDirectory=/opt/NOAA/website
ExecStart=/opt/NOAA/venv/bin/python3 /opt/NOAA/website/app.py

[Install]
WantedBy=multi-user.target
```

Edit file with your personnal information :

> In `/opt/NOAA/website/app.py` with creds of your database

> In `/opt/NOAA/scripts/get_next_pass.py`, edit the last 3 values in function with : your GTM+?, latitude, longitude

> In `/opt/NOAA/scripts/check_pass.sh`, edit mysql command with creds of your database


Setup scan check every minute, run `crontab -e` and add `* * * * * bash /opt/NOAA/scripts/check_pass.sh` at the end

Setup green led in crontab, add `@reboot echo none > /sys/class/leds/ACT/trigger`

Enable and start website 

```bash
systemctl daemon-reload
systemctl enable noaa_web
systemctl start noaa_web
```

And ... VOILA, you can access to images at `http://<ip>:5000` ....
