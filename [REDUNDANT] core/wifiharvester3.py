from m5stack import lcd
from m5stack import *
import network
import utime as time
import ujson as json
import ubinascii
import uos as os


def init_core():
    lcd.set_bg(0x222222)
    lcd.clear()
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setCursor(0, 0)
    lcd.print("launching WiFiHarvester3\n (core=M5Stack Core/Core2)\n")
    lcd.font(lcd.FONT_Ubuntu)


def core2_sleep():
    # lcd.rect(0, 100, 1, 140, lcd.RED, lcd.RED)
    if power.getChargeState():
        lcd.circle(310, 230, 5, lcd.RED, lcd.RED)
        time.sleep(2)
        lcd.circle(310, 230, 5, lcd.RED, lcd.BLACK)
    else:
        lcd.circle(310, 230, 5, lcd.GREEN, lcd.BLACK)
        time.sleep(5)
        lcd.circle(310, 230, 6, lcd.BLACK, lcd.BLACK)


# def sleep(model):
#     pass


def core_notification(message):
    x = 280
    y = 220
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.text(x, y, message)


def core_erase_notification(message):
    x = 280
    y = 220
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.textClear(x, y, message)


def core_printlist(*args):
    for i in args:
        lcd.print(str(i) + " ")


def core_printlistln(*args):
    core_printlist(*args)
    lcd.print("\n")


def str_space(data):
    return str(data) + " "


def draw_core2(stations_db, new_stations, familiar_stations, unique_ssid):
    width, height = lcd.screensize()
    lcd.clear(lcd.BLACK)
    lcd.font(lcd.FONT_DejaVu40)
    lcd.line(0, 50, 320, 50)
    lcd.line(0, 100, 320, 100)
    lcd.line(160, 0, 160, 100)

    # new_stations = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven")
    width_segment = int(width / 2)
    height_segment = 50
    quadrants = [
        (0, 0, width_segment, height_segment, stations_db),
        (width_segment, 0, width, height_segment, unique_ssid),
        (0, 0, width_segment, height_segment * 2, familiar_stations),
        (width_segment, 0, width, height_segment * 2, new_stations),
    ]
    for quadrant in quadrants:
        one, two, three, four, val = quadrant
        lcd.setwin(one, two, three, four)
        lcd.text(lcd.CENTER, lcd.BOTTOM, str(len(val)))
        lcd.resetwin()

    lcd.font(lcd.FONT_Ubuntu)
    lcd.text(1, 35, "AP")
    lcd.text(161, 35, "SSID")
    lcd.text(1, 85, "Cf")
    lcd.text(170, 85, "Cn")

    lcd.setCursor(0, 110)
    lcd.font(lcd.FONT_Ubuntu)
    max_lines = 10
    for y, ssid in enumerate(sorted(new_stations)):
        # if y == max_lines:
        #     lcd.setwin(160, 110, width, height)
        #     lcd.rect(160, 110, 160, 120, lcd.BLACK, lcd.BLACK)
        if y == max_lines:
            break
        lcd.print(ssid + "\n")
        # lcd.resetwin()


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
    core_notification("backup")
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
    core_erase_notification("backup")
    core_notification("saving")
    try:
        with open(filename, "w+") as f:
            json.dump(content, f)
    except Exception:
        core_erase_notification("saving")
        core_notification("s-failed")
        time.sleep(1)


def get_unique_ssid(data):
    return set([data[entry]["ssid"] for entry in data])


stations_filename = "/sd/stations.json"
devinfo_filename = "/sd/devid.json"
authmode_choices = {
    0: "open",
    1: "WEP",
    2: "WPA-PSK",
    3: "WPA2-PSK",
    4: "WPA/WPA2-PSK",
}
changes = False

# Start
init_core()
core_printlistln("\nHardware component:")
core_printlist(" loading", devinfo_filename, "...")
d = load_json(devinfo_filename)
core_printlistln("loaded")
devid = d.get("devID", "unknown")
core_printlistln(" ID:", devid)
devmodel = d.get("model", "unknown")
core_printlistln(" model:", devmodel)

core_printlistln("\nData component:")
core_printlist(" loading", stations_filename, "...")
stations_db = load_json(stations_filename)

core_printlistln("loaded", len(stations_db), "entries")
core_printlist(" populating unique SSID db ...")
unique_ssid = get_unique_ssid(stations_db)
core_printlistln("populated with", len(unique_ssid), "entries")

core_printlist("\nSetting variables ...")
sta = network.WLAN(network.STA_IF)
sta.active(True)
core_printlistln("done")
time.sleep(2)
new_stations = set()
new_stations_session_buffer = set()


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
            core_notification("saving")
            write_json(stations_filename, stations_db)
            core_notification("saving")
            new_stations.add(ssid)
            new_stations_session_buffer = new_stations
            changes = True
        else:
            if ssid in new_stations_session_buffer:
                new_stations.add(ssid)
            else:
                familiar_stations.add(ssid)
            if (
                len(familiar_stations) != nr_familiar_statons_buffer
                or len(new_stations) != nr_new_stations_buffer
            ):
                changes = True

    # now draw it
    if changes:
        draw_core2(stations_db, new_stations, familiar_stations, unique_ssid)
    # def is_highspeed():
    # return True if power.getChargeState() == 1 or power.getBatVoltage() > 4 else False
    # if devmodel == "M5Core2":
    #     core2_sleep()
    # if devmodel == "M5Fire":
    #     fire_sleep()

    core2_sleep()