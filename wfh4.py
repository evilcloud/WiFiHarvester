from m5stack import *
import network
import utime as time
import ubinascii
import csvmp
import core as dev


def get_unique_ssid(data):
    return set([data[entry]["ssid"] for entry in data])


def list_to_dict(data):
    return {
        "bssid": data[0],
        "ssid": data[1],
        "channel": data[2],
        "authmode": data[3],
        "hidden": data[4],
        "devid": data[5],
    }


def dict_to_list(data):
    return [
        data.get("bssid", None),
        data.get("ssid", None),
        data.get("channel", None),
        data.get("authmode", None),
        data.get("hidden", None),
        data.get("devID", None),
    ]


stations_filename = "/sd/stations.csv"
devinfo_filename = "/sd/devid.json"

# Initialization
dev.init()
dev.cprintln("\nHardware component:")
dev.cprintln(" loading", devinfo_filename, "...")
d = dev.load_json(devinfo_filename)
dev.cprintln("loaded")
devid = d.get("devID", "unknown")
dev.cprintln(" ID:", devid)
devmodel = d.get("model", "unknown")
dev.cprintln(" model:", devmodel)

dev.cprintln("\nData component:")
dev.cprintln(" loading", stations_filename, "...")

stations_db = {}

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
new_entries = []  # buffer for the newly discovered stations to be added to csv list
cycles = 0
save_freq = 3
dev.cprintln("done")
dev.csleep(2)

# Let's go!
dev.cclear()
dev.draw_grid()
dev.draw_ap(len(stations_db))
dev.draw_ssid(len(unique_ssid))
while True:
    cycles += 1
    dev.draw_cycles(cycles, True)
    dev.draw_cycles(cycles)
    current_scan = sta.scan()
    familiar_stations = set()
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

            new_entries.append(dict_to_list(stations_db[bssid]))
            new_stations.add(ssid)
            new_stations_session_buffer = new_stations
        else:
            if ssid in new_stations_session_buffer:
                new_stations.add(ssid)
                # dev.draw_cnew(len(new_stations))
            else:
                familiar_stations.add(ssid)
                # dev.draw_cfamiliar(len(familiar_stations))
    # Show and save changes
    if len(familiar_stations) != nr_familiar_statons_buffer:
        dev.draw_cfamiliar(len(familiar_stations))
    if len(new_stations) != nr_new_stations_buffer:
        dev.draw_cnew(len(new_stations))
        dev.draw_ssids(new_stations)
    if len(new_entries) and cycles % save_freq == 0:
        csvmp.add(new_entries, stations_filename)
        new_entries = []
        dev.draw_ap(len(stations_db))