from m5stack import *
import network
import utime as time
import ubinascii
import csvmp
import core as dev

# Core display specific
from m5stack import lcd


def cprint(*args):
    # lcd.print(" ".join([str(i) for i in args]))
    for i in args:
        lcd.print(str(i) + " ")


def cprintln(*args):
    cprint(*args)
    lcd.print("\n")


# Platform agnostic


def load_prev_csv(stations_filename):
    """loads CSV file (external module) and returns unique BSSIDs and SSIDs

    Args:
        stations_filename (str): the name of the CSV file

    Returns:
        tuple (set, set): a list of unique BSSID and SSID values from the file
    """
    bssid_db = set()
    # unique_ssid_db = set()
    b = csvmp.read(stations_filename)
    dev.cprint("[")
    for i, entry in enumerate(b):
        if len(entry) > 2:
            bssid_db.add(entry[0])
            # unique_ssid_db.add(entry[1])
            if i % (100 / len(entry)) == 0:
                cprint(".")
        else:
            break
    return bssid_db  # , unique_ssid_db


def initialize(stations_filename, devinfo_filename):
    dev.initialize()
    cprintln("\nHardware component:")
    cprint(" loading", devinfo_filename, "...")
    d = dev.load_json(devinfo_filename)
    cprintln("loaded")
    devid = d.get("devID", "unknown")
    cprintln(" ID:", devid)
    devmodel = d.get("model", "unknown")
    cprintln(" model:", devmodel)
    cprintln("\nData component:")
    cprintln(" loading", stations_filename, "...")
    return devid


stations_filename = "/sd/stations.csv"
devinfo_filename = "/sd/devid.json"

devid = initialize(stations_filename, devinfo_filename)
dev.cprintln(" loading previous records")
bssid_db = load_prev_csv(stations_filename)  # and unique_ssid_db
dev.cprintln(" BSSID:", len(bssid_db))  # , ", SSID:", len(unique_ssid_db))

# Setting up variables before the launch
dev.cprint("\nSetting variables ...")
sta = network.WLAN(network.STA_IF)
sta.active(True)


new_stations_session_buffer = set()
authmode_choices = {
    0: "open",
    1: "WEP",
    2: "WPA-PSK",
    3: "WPA2-PSK",
    4: "WPA/WPA2-PSK",
}
new_entries = set()  # buffer for the newly discovered stations to be added to csv list
unfamiliar_ssids = set()
familiar_ssids = set()
cycles = 0
cycle_rec_frequency = 10
# unique_ssid_nr = 0
new_bssids_rec_trigger = 60
dev.cprintln("done")
dev.csleep(2)

# Let's go!
dev.cclear()
dev.draw_grid()
# We already have the values of these two, even if they are 0
dev.draw_ap(len(bssid_db))
# dev.draw_ssid(len(unique_ssid_db))

while True:
    cycles += 1
    dev.draw_cycle(cycles)
    # dev.draw_cycles(cycles, True)
    # dev.draw_cycles(cycles)
    current_scan = sta.scan()

    for station in current_scan:
        bssid = ubinascii.hexlify(station[1]).decode()
        ssid = station[0].decode()
        channel = str(station[2])
        authmode = authmode_choices.get(station[4])
        hidden = str(station[5])

        if bssid not in bssid_db:
            bssid_db.add(bssid)
            dev.draw_ap(len(bssid_db))

            new_entries.add((bssid, ssid, channel, authmode, hidden))
            unfamiliar_ssids.add(ssid)
            dev.draw_cnew(len(unfamiliar_ssids))

            # unique_ssid_db.add(ssid)
            # if len(unique_ssid_db) > unique_ssid_nr:
            #     dev.draw_ssid(unique_ssid_nr)
            #     unique_ssid_nr = len(unique_ssid_db)
        else:
            familiar_ssids.add(ssid)
            dev.draw_cfamiliar(len(familiar_ssids))
    if unfamiliar_ssids:
        dev.draw_ssids(unfamiliar_ssids)

    if cycles % cycle_rec_frequency == 0 or len(bssid_db) % new_bssids_rec_trigger == 0:
        err = csvmp.add(new_entries, stations_filename)
        if not err:
            new_entries.clear()
    # reset fam/unfam buffer each cycle, because why would we need to carry it with us?
    unfamiliar_ssids.clear()
    familiar_ssids.clear()
