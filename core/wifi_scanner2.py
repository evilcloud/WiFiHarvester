from m5stack import *
import network
import utime as time
import ubinascii
import ujson as json


def show_list(stations):
    for line in lines:
        lcd.print(line + "\n")


def read_json(filename):
    try:
        with open(filename) as fs:
            return json.load(fs)
    except Exception:
        f = open(filename, "w+")
        f.write("")
        f.close()
        return {}


def write_json(filename, data):
    err = ""
    try:
        with open(filename, "w+") as fs:
            json.dump(data, fs)
    except Exception as e:
        err = e
    return err


def batt_level():
    battery = ""
    # battery = ""
    # if power.isCharging():
    #     battery = "charging"
    # if power.isCharged():
    #     battery = battery + " 100%"
    # if not battery:
    #     battery = power.getBatteryLevel()
    return battery


def connect_and_upload():
    wifiCfg.autoConnect(lcdShow=True)


lcd.clear()
lcd.fontSize(10)


stations_filename = "/sd/stations.json"
sta = network.WLAN(network.STA_IF)
sta.active(True)

stations_full = read_json(stations_filename)

authmode_choices = {0: "open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}

hidden_choices = {0: " ", 1: " X "}

nr = 0
new = False
lines = []
wifi_buffer = None
while True:
    nr_buffer = nr
    wifi_list = sta.scan()
    for station in wifi_list:
        ssid = station[0].decode()
        bssid = ubinascii.hexlify(station[1]).decode()
        channel = station[2]
        authmode = station[4]
        hidden = station[5]
        if not stations_full.get(bssid):
            line = (
                str(channel)
                + " "
                + ssid
                + hidden_choices.get(hidden)
                + authmode_choices.get(authmode)
            )
            lcd.print(line + "\n")
            stations_full[bssid] = [ssid, bssid, channel, authmode, hidden]
            new = True
            lines.append(line)
            if len(lines) > 15:
                lines = lines[1:]
    if new:
        _ = write_json(stations_filename, stations_full)
        # show_list(lines)
        new = False
        lcd.clear()
        lcd.font(lcd.FONT_Default)
        lcd.fontSize(10)
        # lcd.font(lcd.FONT_DejaVu24)
        lcd.setCursor(0, 0)
        lcd.print("total: " + str(len(stations_full)) + "\t" + batt_level() + "\n\n")
        show_list(lines)
    time.sleep(10)
