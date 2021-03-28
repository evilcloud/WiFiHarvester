from m5stack import *
import utime as time
import ujson as json
import network


def get_devid(model="unknown"):
    d = read_json("/sd/devid.json")
    return d["devID"] if d else model


def read_json(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except Exception:
        write_json(filename, {})


def write_json(filename, data):
    try:
        with open(filename, "w+") as f:
            json.dump(data, f)
    except Exception as err:
        return str(err)

def scan_stations(sta):
    wifi_list = sta.scan()
    for station in wifi_list:
        ssid = station[0].decode()
        bssid = ubinascii.hexlify(station[1]).decode()
        channel = station[2]
        authmode = authmode_choices.get(station[4])
        hidden = station[5]
    return wifi_list


def main_loop(devid):
    stations_file = "/sd/stations.json"
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    all_stations = read_json(stations_file)
    
    wifi_list = scan_stations(sta)
    
    while True:

        if not all_stations.get(bssid):
            all_stations[bssid] = {
                "ssid": ssid,
                "bssid": bssid,
                "channel": channel,
                "authmode": authmode,
                "hidden": hidden,
                "count": count,
                "devID": devid,
            }

if __name__ == "__main__":
    pass