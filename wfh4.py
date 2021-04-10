from m5stack import *
import network
import utime as time
import ubinascii
import csvmp

# HARDWARE CHOICES
import core as dev

# import stickc as dev
# import ink as dev


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
            if i % (50 / len(entry)) == 0:
                dev.cprint(".")
        else:
            break
    dev.cprintln("]")
    return bssid_db  # , unique_ssid_db


def format_error(error, cycle):
    """returns a formated log entry for further saving

    Args:
        error (any): the error message
        cycle (int): the cycle number

    Returns:
        str: formated string with leading ==== and a break at the end
    """
    return "=====\nCycle " + str(cycle) + "\n" + str(error) + "\n\n"


def initialize(stations_filename, devinfo_filename):
    dev.initialize()
    dev.cprintln("\nHardware component:")
    dev.cprint(" loading", devinfo_filename, "...")
    d, msg = dev.load_json(devinfo_filename)
    dev.cprintln(msg)
    devid = d.get("devID", "unknown")
    dev.cprintln(" ID:", devid)
    devmodel = d.get("model", "unknown")
    dev.cprintln(" model:", devmodel)
    dev.cprintln("\nData component:")
    # dev.cprintln(" loading", stations_filename, "...")
    return devid


stations_filename = "/flash/stations.csv"
devinfo_filename = "/flash/devid.json"
err_log_filename = "/flash/err.log"

devid = initialize(stations_filename, devinfo_filename)
dev.cprintln(" loading previous records")
bssid_db = load_prev_csv(stations_filename)  # and unique_ssid_db
dev.cprintln(" BSSID:", len(bssid_db))  # , ", SSID:", len(unique_ssid_db))

# Setting up variables before the launch
dev.cprint("\nSetting variables ...")
sta = network.WLAN(network.STA_IF)
sta.active(True)

# Service variables
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

# unique_ssid_nr = 0

# Setting variables
cycle_rec_frequency = 10
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
    try:
        dev.draw_dot_scan("yellow")
        current_scan = sta.scan()
        # dev.draw_status("scanned")
        dev.draw_dot_scan("black")
    except Exception as e:
        dev.draw_status("scan error " + str(cycles))
        dev.draw_dot_scan("red")
        err = format_error(e, cycles)
        dev.add(err_log_filename, err)
    dev.draw_cycle(str(cycles))
    for i, station in enumerate(current_scan):
        dev.draw_bssid_loop(str(i + 1) + "/" + str(len(current_scan)))
        # dev.draw_status("looping " + str(i + 1) + " of " + str(len(current_scan)))
        bssid = ubinascii.hexlify(station[1]).decode()
        ssid = station[0].decode()
        channel = str(station[2])
        authmode = authmode_choices.get(station[4])
        hidden = str(station[5])

        if bssid not in bssid_db:
            # dev.draw_status(str(bssid))
            bssid_db.add(bssid)
            dev.draw_ap(len(bssid_db))

            new_entries.add((bssid, ssid, channel, authmode, hidden))
            unfamiliar_ssids.add(ssid)
        else:
            familiar_ssids.add(ssid)
    if unfamiliar_ssids:
        dev.draw_cnew(len(unfamiliar_ssids))
        dev.draw_ssids(unfamiliar_ssids)

    if familiar_ssids:
        dev.draw_cfamiliar(len(familiar_ssids))

    if new_entries and (
        cycles % cycle_rec_frequency == 0 or len(bssid_db) % new_bssids_rec_trigger == 0
    ):
        dev.draw_dot_save("yellow")
        # dev.draw_status("saving" + str(len(new_entries)) + " stations")
        err = csvmp.add(new_entries, stations_filename)
        if not err:
            dev.draw_dot_save("black")
            new_entries.clear()
        else:
            dev.draw_dot_save("red")
            dev.draw_status("error saving cy " + str(cycles))
            dev.add(err_log_filename, format_error(err, cycles))

    # reset fam/unfam buffer each cycle, because why would we need to carry it with us?
    unfamiliar_ssids.clear()
    familiar_ssids.clear()
