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
# Retrieve project
git clone https://github.com/Noderyos/NOAA-Tracker /opt/NOAA

# Setup
cd /opt/NOAA
mkdir images
python3 -m venv venv
source venv/bin/activate
pip -r requirements.txt
```

# Create website service

In `/etc/systemd/system/noaa_web.service`, put

```
tee -a /etc/systemd/system/noaa_web.service << END
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

Setup scan check every minute, run `crontab -e` and add `* * * * * bash /opt/NOAA/scripts/check_pass.sh` at the end

Setup green led in crontab, add `@reboot echo none > /sys/class/leds/ACT/trigger`

Enable and start website 

```bash
systemctl daemon-reload
systemctl enable noaa_web
systemctl start noaa_web
```
