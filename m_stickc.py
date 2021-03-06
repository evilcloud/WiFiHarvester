from m5stack import *
import network
import utime as time
import ubinascii
import csvmp

# HARDWARE CHOICES
# import core as dev
import stickc as dev


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


def cclear(color=lcd.BLACK):
    lcd.clear(color)


def cprint(*args):
    # lcd.print(" ".join([str(i) for i in args]))
    for i in args:
        lcd.print(str(i) + " ")


def cprintln(*args):
    cprint(*args)
    lcd.print("\n")


def initialize(stations_filename, devinfo_filename):
    lcd.clear(lcd.BLACK)
    # lcd.font(lcd.FONT_DejaVu18)
    lcd.setCursor(0, 0)
    lcd.print("launching WiFiHarvester 3.2\non StickC (Plus) LoboMP device\n")
    # lcd.font(lcd.FONT_Ubuntu)

    cprintln("\nHardware component:")
    cprint(" loading", devinfo_filename, "...")
    d, msg = dev.load_json(devinfo_filename)
    cprintln(msg)
    devid = d.get("devID", "unknown")
    cprintln(" ID:", devid)
    devmodel = d.get("model", "unknown")
    cprintln(" model:", devmodel)
    cprintln("\nData component:")
    # dev.cprintln(" loading", stations_filename, "...")
    return devid


stations_filename = "/flash/stations.csv"
devinfo_filename = "/flash/devid.json"

devid = initialize(stations_filename, devinfo_filename)
cprintln(" loading previous records")
bssid_db = load_prev_csv(stations_filename)  # and unique_ssid_db
cprintln(" BSSID:", len(bssid_db))  # , ", SSID:", len(unique_ssid_db))

# Setting up variables before the launch
cprint("\nSetting variables ...")
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
cprintln("done")
csleep(2)

# Let's go!
cclear()
draw_grid()
# We already have the values of these two, even if they are 0
draw_ap(len(bssid_db))
# dev.draw_ssid(len(unique_ssid_db))

while True:
    cycles += 1
    current_scan = sta.scan()
    dev.draw_cycle("S " + str(len(current_scan)) + "  C " + str(cycles))
    # dev.reset_progress_bar()
    for i, station in enumerate(current_scan):
        # dev.draw_progress_line(i)
        dev.draw_status("looping " + str(i + 1) + " of " + str(len(current_scan)))
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

            # unique_ssid_db.add(ssid)
            # if len(unique_ssid_db) > unique_ssid_nr:
            #     dev.draw_ssid(unique_ssid_nr)
            #     unique_ssid_nr = len(unique_ssid_db)
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
        dev.draw_status("saving" + str(len(new_entries)) + " stations")
        err = csvmp.add(new_entries, stations_filename)
        if not err:
            dev.draw_status("saved " + str(len(new_entries)) + " stations")
            new_entries.clear()
        else:
            dev.draw_status("error saving. data cached")

    # reset fam/unfam buffer each cycle, because why would we need to carry it with us?
    unfamiliar_ssids.clear()
    familiar_ssids.clear()
