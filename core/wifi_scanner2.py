from m5stack import *
import network
import utime as time
import ubinascii
import ujson as json


def show_list(stations):
    for line in lines:
        lcd.print(line + "\n")


# def reformat_stationslist(bssid_dict, key):
#     new_dict = {}
#     for entry in bssid_list:
#         e = data[entry]
#         ssid = e["ssid"]
#         authmode = e["authmode"]
#         hidden = e["hidden"]
#         count = e["count"]
#         channel = e["channel"]
#         devid = e["devID"]
#         bssid = entry
#         new_dict[key] = {
#             "ssid": ssid,
#             "bssid": bssid,
#             "channel": channel,
#             "authmode": authmode,
#             "hidden": hidden,
#             "count": count,
#             "devID": devid,
#         }
#     return new_dict


def get_devid(model="unknown"):
    d = read_json("/sd/devid.json")
    return d["devID"] if d else model


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


# def is_gesture():
#     if touch.status() == 1:


def get_unique_ssid(data):
    ussid = set()
    for entry in data:
        ussid.add(data[entry]["ssid"])
    return ussid


def is_highspeed():
    return True if power.getChargeState() == 1 or power.getBatVoltage() > 4 else False


# def connect_and_upload():
#     wifiCfg.autoConnect(lcdShow=True)


lcd.clear()
lcd.font(lcd.FONT_DejaVu18)
d = read_json("/sd/devid.json")
devid = get_devid()
lcd.print("launching Wifi scanner 2\n")
lcd.print("DevID: " + devid + "\n")

stations_filename = "/sd/stations.json"
stations_full = read_json(stations_filename)
lcd.print("Currently harvested\n")
lcd.print("  Individual AP: " + str(len(stations_full)) + "\n")
lcd.print("   Unique SSID: " + str(len(get_unique_ssid(stations_full))) + "\n\n")

fast_scan = 1
slow_scan = 3
sta = network.WLAN(network.STA_IF)
sta.active(True)


authmode_choices = {0: "open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}
hidden_choices = {0: " ", 1: " X "}

premitted_screenlines = 15
new = False
lines = []
wifi_buffer = None

# scan_speed = fast_scan if is_highspeed() else slow_scan
# scan_buffer = scan_speed
scan_speed = 1
lcd.print("Scan speed: " + str(scan_speed) + "\n")
while True:
    power.setPowerLED(False)
    # if scan_buffer != scan_speed:
    #     lcd.clear()
    #     lcd.print("New scanspeed: " + str(scan_speed))
    # scan_speed = fast_scan if is_highspeed() else slow_scan
    # scan_buffer = scan_speed

    # nr_buffer = nr
    scan_speed = fast_scan if is_highspeed() else slow_scan
    wifi_list = sta.scan()
    for station in wifi_list:
        ssid = station[0].decode()
        bssid = ubinascii.hexlify(station[1]).decode()
        channel = station[2]
        authmode = authmode_choices.get(station[4])
        hidden = station[5]
        count = len(stations_full)
        if not stations_full.get(bssid):
            line = (
                ("0" + str(channel))[:2]
                + " "
                + ssid
                + hidden_choices.get(hidden)
                + authmode
            )
            lcd.print(line + "\n")
            stations_full[bssid] = {
                "ssid": ssid,
                "bssid": bssid,
                "channel": channel,
                "authmode": authmode,
                "hidden": hidden,
                "count": count,
                "devID": devid,
            }
            new = True
            lines.append(line)
            if len(lines) > premitted_screenlines:
                lines = lines[1:]
    if new:
        power.setPowerLED(False)
        _ = write_json(stations_filename, stations_full)
        new = False
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.font(lcd.FONT_DejaVu24)
        lcd.print(
            "total: "
            + str(len(stations_full))
            + "  unique: "
            + str(len(get_unique_ssid(stations_full)))
            + "  "
            + str(scan_speed)
            + "s\n"
        )
        lcd.font(lcd.FONT_Default)
        lcd.fontSize(10)
        show_list(lines)
    time.sleep(scan_speed)
