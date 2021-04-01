from m5stack import lcd
from m5stack import *
import network
import utime as time
import ujson as json
import ubinascii
import uos as os

import core as dev


# def core2_sleep():
#     if power.getChargeState():
#         lcd.circle(310, 230, 5, lcd.RED, lcd.RED)
#         time.sleep(2)
#         lcd.circle(310, 230, 5, lcd.RED, lcd.BLACK)
#     else:
#         lcd.circle(310, 230, 5, lcd.GREEN, lcd.BLACK)
#         time.sleep(5)
#         lcd.circle(310, 230, 6, lcd.BLACK, lcd.BLACK)


def load_json(filename):
    content = {}
    try:
        with open(filename) as f:
            content = json.load(f)
    except Exception:
        write_json(filename, content)
    return content


def write_json(filename, content):
    # existing backup file
    dev.notify("backup")
    backup_name = "/sd/backup.json"
    try:
        os.remove(backup_name)
    except:
        pass
    try:
        f = open(filename)
        f.close()
        os.rename(filename, backup_name)
    except:
        pass
    dev.unnotify("backup")
    dev.notify("saving")
    try:
        with open(filename, "w+") as f:
            json.dump(content, f)
    except Exception:
        dev.unnotify("saving")
        dev.notify("s-failed")
        time.sleep(1)


def get_unique_ssid(data):
    return set([data[entry]["ssid"] for entry in data])




stations_filename = "/sd/stations.json"
devinfo_filename = "/sd/devid.json"

# Initialization
dev.init()
dev.cprintln("\nHardware component:")
dev.cprint(" loading", devinfo_filename, "...")
d = load_json(devinfo_filename)
dev.cprintln("loaded")
devid = d.get("devID", "unknown")
dev.cprintln(" ID:", devid)
devmodel = d.get("model", "unknown")
dev.cprintln(" model:", devmodel)

dev.cprintln("\nData component:")
dev.cprint(" loading", stations_filename, "...")
stations_db = load_json(stations_filename)

dev.cprintln("loaded", len(stations_db), "entries")
dev.cprint(" populating unique SSID db ...")
unique_ssid = get_unique_ssid(stations_db)
dev.cprintln("populated with", len(unique_ssid), "entries")

# Setting up variables before the launch
dev.cprint("\nSetting variables ...")
sta = network.WLAN(network.STA_IF)
sta.active(True)
new_stations_session_buffer = set()
nr_unique_ssid_buffer = 0
authmode_choices = {
    0: "open",
    1: "WEP",
    2: "WPA-PSK",
    3: "WPA2-PSK",
    4: "WPA/WPA2-PSK",
}
dev.cprintln("done")
time.sleep(2)

# Let's go!
dev.cclear()
dev.draw_ap(len(stations_db))
dev.draw_ssid(len(unique_ssid))
while True:
    current_scan = sta.scan()
    familiar_stations = (
        set()
    )  # resetting the new stations list (buffer will come later)
    new_stations = set()
    

    for station in current_scan:
        nr_familiar_statons_buffer = len(familiar_stations)
        nr_new_stations_buffer = len(new_stations)
        ssid = station[0].decode()
        bssid = ubinascii.hexlify(station[1]).decode()
        channel = station[2]
        authmode = authmode_choices.get(station[4])
        hidden = station[5]
        count = len(stations_db)

        unique_ssid.add(ssid)
        n = len(unique_ssid)
        if nr_unique_ssid_buffer != n:
            dev.draw_ssid(n)
            nr_unique_ssid_buffer = n

        # Make sure to keep new stations in the list if they have not dissapeared
        if bssid in new_stations_session_buffer:
            new_stations.add(bssid)

        if not stations_db.get(bssid):
            stations_db[bssid] = {
                "ssid": ssid,
                "bssid": bssid,
                "channel": channel,
                "authmode": authmode,
                "hidden": hidden,
                "count": count,
                "devID": devid,
            }
            dev.notify("saving")
            write_json(stations_filename, stations_db)
            dev.unnotify("saving")
            new_stations.add(ssid)
            dev.draw_ssids(new_stations)
            new_stations_session_buffer = new_stations
        else:
            if ssid in new_stations_session_buffer:
                new_stations.add(ssid)
                # dev.draw_cnew(len(new_stations))
            else:
                familiar_stations.add(ssid)
                # dev.draw_cfamiliar(len(familiar_stations))
    if len(familiar_stations) != nr_familiar_statons_buffer:
        dev.draw_cfamiliar(len(familiar_stations))
    if len(new_stations) != nr_new_stations_buffer:
        dev.draw_cnew(len(new_stations))
    