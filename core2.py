from m5stack import *
import time
import core


def init():
    core.init()


def cclear():
    core.clear()


def cprint(*args):
    core.cprint(*args)


def cprintln(*args):
    core.cprintln(*args)


def draw_grid():
    core.draw_grid()


def draw_indicators(indicator, value):
    core.draw_indicators(indicator, value)


def get_text_halfwidth(text):
    return core.get_text_halfwidth(text)


def draw_ap(value):
    core.draw_ap(value)


def draw_ssid(value):
    core.draw_ssid(value)


def draw_cfamiliar(value):
    core.draw_cfamiliar(value)


def draw_cnew(value):
    core.draw_cnew(value)


def draw_ssids(valuelist):
    core.draw_ssids(valuelist)


def notify(message):
    core.notify(message)


def unnotify(message):
    core.unnotify(message)


def sleep_notice():
    core.sleep_notice()


def csleep(t, powered=False):
    powered = powered if powered else t
    if power.getChargeState():
        lcd.circle(310, 230, 5, lcd.RED, lcd.RED)
        time.sleep(powered)
        lcd.circle(310, 230, 5, lcd.RED, lcd.BLACK)
    else:
        core.csleep(t)


# ========================= FS stuff ========================================


def load_json(filename):
    return core.load_json(filename)


def write_json(filename, content):
    core.write_json(filename, content)


# ========================= TEST stuff =================================


cclear()
# lcd.restorewin()
draw_ap(9999)
draw_ssid(9999)
draw_cfamiliar(9999)
draw_cnew(9999)
notify("something")
draw_ssids(
    [
        "DIRECT-35-HP ENVY 4520 series",
        "midr-cardvr-v1_midev16d8",
        "_FREEAdWiFi_4CatsPantry",
        "Tortoise Sand Network",
        "micfongkc",
        "IBR600-41c",
        "ShelleyChan",
        "TP-Link_1FC8",
        "IROAD_X5_2F127",
        "MyDean 3e070f",
        "無法識別訊號",
        "Haymarket_Laptop",
        "DBS_Guest_Wi-Fi",
        "HKBN-BD0661-Guest",
        "island-296BB0",
        "sanodance-Guest",
        "Eat_Kitchen_2.4G",
        "SpaceStore_Guest",
        "26G Home 5G",
    ]
)
time.sleep(5)
unnotify("something")
sleep_notice()
