from m5stack import *
import ujson as json
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


def draw_indicators(indicator, value):
    tvalue = str(value)
    coordinates = {
        "AP": (0, 0, 160, 50),
        "SSID": (160, 0, 160, 50),
        "Cf": (0, 50, 160, 50),
        "Cn": (160, 50, 160, 50),
    }
    x, y, x2, y2 = indicator.get(coordinates)
    text = str(value)
    text_halfwidth = int(lcd.textWidth(text) / 2)
    lcd.rect(x, y, x2, y2)
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.text(x + 2, y + 2, text)
    lcd.font(lcd.FONT_DejaVu40)
    lcd.text(x + (x2 - text_halfwidth), y + 5, text)


def get_text_halfwidth(text):
    return int(lcd.textWidth(str(text)) / 2)


def draw_ap(value):
    lcd.rect(0, 0, 160, 50, lcd.BLACK, lcd.BLACK)
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.text(1, 1, "AP")
    lcd.font(lcd.FONT_DejaVu40)
    text = str(value)
    lcd.text(int((320 / 4) - get_text_halfwidth(text)), 10, str(text))


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


def csleep(t):
    lcd.circle(310, 230, 5, lcd.GREEN, lcd.BLACK)
    time.sleep(t)
    lcd.circle(310, 230, 6, lcd.BLACK, lcd.BLACK)


# ========================= FS stuff ========================================


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
    dev.notify("backup")
    backup_name = "/sd/backup"
    filelist = os.listdir()
    for i in range(100):
        construct = backup_name + str(i) + ".json"
        if construct not in filelist:
            backup_name = construct
    else:
        try:
            os.remove(backup_name + ".json")
            backup_name = backup_name + ".json"
        except:
            pass
    try:
        f = open(filename)
        f.close()
        os.rename(filename, backup_name)
    except:
        pass
    dev.unnotify("backup")
    dev.notify("saving")
    try:
        with open(filename, "w+") as f:
            json.dump(content, f)
    except Exception:
        dev.unnotify("saving")
        dev.notify("s-failed")
        time.sleep(1)


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
