from m5stack import *
import time
from m5stack import lcd
from m5stack import *
import network
import utime as time
import ujson as json
import ubinascii
import uos as os


def init():
    lcd.clear(lcd.BLACK)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setCursor(0, 0)
    lcd.print("launching WiFiHarvester 3.2\non Core/Core2 LoboMP device\n")
    lcd.font(lcd.FONT_Ubuntu)


def cclear():
    lcd.clear(lcd.BLACK)


def cprint(*args):
    for i in args:
        lcd.print(str(i) + " ")


def cprintln(*args):
    cprint(*args)
    lcd.print("\n")


def draw_grid():from m5stack import *
import time


def init():
    lcd.clear(lcd.BLACK)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setCursor(0, 0)
    lcd.print("launching WiFiHarvester 3.2\non Core/Core2 LoboMP device\n")
    lcd.font(lcd.FONT_Ubuntu)


def cclear(color=lcd.BLACK):
    lcd.clear(color)


def cprint(*args):
    for i in args:
        lcd.print(str(i) + " ")


def cprintln(*args):
    cprint(*args)
    lcd.print("\n")


def draw_grid():
    lcd.line(0, 50, 320, 50)
    lcd.line(0, 100, 320, 100)
    lcd.line(160, 0, 160, 100)


def get_text_halfwidth(text):
    return int(lcd.textWidth(str(text)) / 2)


def draw_ap(value):
    lcd.rect(0, 0, 160, 50, lcd.BLACK, lcd.BLACK)
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.text(1, 1, "AP")
    lcd.font(lcd.FONT_DejaVu40)
    text = str(value)
    lcd.text(int((320 / 4) - get_text_halfwidth(value)), 10, str(value))


def draw_ssid(value):
    lcd.rect(160, 0, 160, 50, lcd.BLACK, lcd.BLACK)
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.text(161, 1, "SSID")
    lcd.font(lcd.FONT_DejaVu40)
    lcd.text(int(((320 / 4) * 3) - get_text_halfwidth(value)), 10, str(value))


def draw_cfamiliar(value):
    lcd.rect(0, 50, 160, 50, lcd.BLACK, lcd.BLACK)
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.text(1, 51, "Cf")
    lcd.font(lcd.FONT_DejaVu40)
    lcd.text(int((320 / 4) - get_text_halfwidth(value)), 60, str(value))


def draw_cnew(value):
    lcd.rect(160, 50, 160, 50, lcd.BLACK, lcd.BLACK)
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.text(161, 51, "Cf")
    lcd.font(lcd.FONT_DejaVu40)
    lcd.text(int(((320 / 4) * 3) - get_text_halfwidth(value)), 60, str(value))


def draw_ssids(valuelist):
    max_lenght = 8
    vert_offset = 15
    x = 0
    y = 110
    lcd.font(lcd.FONT_Ubuntu)
    # lcd.setwin(0, 110, 160, 230)
    lcd.rect(0, 105, 320, 130, lcd.BLACK, lcd.BLACK)
    for i, text in enumerate(valuelist):
        if i == max_lenght:
            lcd.rect(160, 105, 160, 230, lcd.BLACK, lcd.BLACK)
            x = 160
            y = 110
        if i == max_lenght * 2:
            break
        text = text[:18] if x else text
        lcd.text(x, y, text)
        y = y + vert_offset


def notify(message):
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.text(250, 220, str(message))


def unnotify(message):
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.textClear(250, 220, str(message))


def sleep_notice():
    lcd.circle(310, 230, 5, lcd.GREEN, lcd.BLACK)
    time.sleep(5)
    lcd.circle(310, 230, 6, lcd.BLACK, lcd.BLACK)

# =================================================================

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
    notify("backup")
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
    unnotify("backup")
    notify("saving")
    try:
        with open(filename, "w+") as f:
            json.dump(content, f)
    except Exception:
        unnotify("saving")
        notify("s-failed")
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
init()
cprintln("\nHardware component:")
cprint(" loading", devinfo_filename, "...")
d = load_json(devinfo_filename)
cprintln("loaded")
devid = d.get("devID", "unknown")
cprintln(" ID:", devid)
devmodel = d.get("model", "unknown")
cprintln(" model:", devmodel)

cprintln("\nData component:")
cprint(" loading", stations_filename, "...")
stations_db = load_json(stations_filename)

cprintln("loaded", len(stations_db), "entries")
cprint(" populating unique SSID db ...")
unique_ssid = get_unique_ssid(stations_db)
cprintln("populated with", len(unique_ssid), "entries")

cprint("\nSetting variables ...")
sta = network.WLAN(network.STA_IF)
sta.active(True)
cprintln("done")
time.sleep(2)
new_stations_session_buffer = set()
nr_unique_ssid_buffer = 0

cclear()
draw_ap(len(stations_db))
draw_ssid(len(unique_ssid))
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
            draw_ssid(n)
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
            notify("saving")
            write_json(stations_filename, stations_db)
            unnotify("saving")
            new_stations.add(ssid)
            new_stations_session_buffer = new_stations
            changes = True
        else:
            if ssid in new_stations_session_buffer:
                new_stations.add(ssid)
                # draw_cnew(len(new_stations))
            else:
                familiar_stations.add(ssid)
                # draw_cfamiliar(len(familiar_stations))
    if len(familiar_stations) != nr_familiar_statons_buffer:
        draw_cfamiliar(len(familiar_stations))
    if len(new_stations) != nr_new_stations_buffer:
        draw_cnew(len(new_stations))
 