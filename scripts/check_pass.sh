#!/bin/bash 

if [[ -f /tmp/receiving ]];then
	exit 2
fi


declare -A satellites=([25338]="NOAA 15" [28654]="NOAA 18" [33591]="NOAA 19")
declare -A frequencies=([25338]=137620000 [28654]=137912500 [33591]=137100000)

for i in "${!satellites[@]}"; do
	cur_date=`date +%s`
	echo "[DEBUG] Checking next pass for ${satellites[$i]}"
	req=`/opt/NOAA/venv/bin/python3 /opt/NOAA/scripts/get_next_pass.py ${i}`
	start_pass=`echo $req | cut -d " " -f1`
	duration=`echo $req | cut -d " " -f2`
	duration=$((duration+200))
	elevation=`echo $req | cut -d " " -f3`
	echo "[DEBUG] Next pass at $start_pass for a duration of ${duration}s at ${elevation}°"

	if [[ $start_pass -gt $cur_date && $((start_pass-cur_date)) -lt 60 ]];then
		touch /tmp/receiving
		echo 1 >/sys/class/leds/ACT/brightness
		echo "[DEBUG] Starting to record with parameters : $i `echo ${satellites[$i]} | cut -d " " -f2` $duration ..."
		d=`date +%s`
		timeout ${duration}s rtl_sdr -f ${frequencies[$i]} -s 250000 /tmp/$d.bin

		rm /tmp/receiving
		echo 0 >/sys/class/leds/ACT/brightness
		satdump noaa_apt baseband /tmp/$d.bin /opt/NOAA/images/$d --samplerate 250000 --baseband_format s8 --sdrpp_noise_reduction --start_timestamp $d --satellite_number `echo ${satellites[$i]} | cut -d ' ' -f2`
		mysql --user=noaa --password=noaa --database=noaa --execute "INSERT INTO pass VALUES (FROM_UNIXTIME($d), \"${satellites[$i]}\", $((duration-200)), $elevation);"
	fi
done

