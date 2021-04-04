import btree


def db_open():
    try:
        f = open("/sd/wft4", "r+b")
    except OSError:
        f = open("/sd/wft4", "w+b")
    f.close()


def add_entry(station):
    f = open("/sd/wft4", "r+b")
    db = btree.open(f)
    bssid = ubinascii.hexlify(station[1]).decode()
    db[bssid] = {
        ssid: station[0].decode(),
        bssid: bssid,
        channel: station[2],
        authmode: authmode_choices.get(station[4]),
        hidden: station[5],
    }
