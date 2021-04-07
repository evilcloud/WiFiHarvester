from m5stack import *
import ujson as json
import time
import uos as os


def initialize():
    lcd.clear(lcd.BLACK)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setCursor(0, 0)
    lcd.print("launching WiFiHarvester 3.2\non Core/Core2 LoboMP device\n")
    lcd.font(lcd.FONT_Ubuntu)


def cclear(color=lcd.BLACK):
    lcd.clear(color)


def cprint(*args):
    # lcd.print(" ".join([str(i) for i in args]))
    for i in args:
        lcd.print(str(i) + " ")


def cprintln(*args):
    cprint(*args)
    lcd.print("\n")


def draw_grid():
    lcd.line(5, 105, 320, 105)
    # lcd.line(0, 50, 320, 50)
    # lcd.line(0, 100, 320, 100)
    # lcd.line(160, 0, 160, 100)


def draw_indicators(indicator, value):
    note = notify("draw indicators")
    coordinates = {
        "AP": (0, 0, 160, 50),
        "SSID": (160, 0, 160, 50),
        "Cf": (0, 50, 160, 50),
        "Cn": (160, 50, 160, 50),
    }
    x, y, x2, y2 = coordinates[indicator]
    text = str(value)
    text_halfwidth = int(lcd.textWidth(text) / 2)
    lcd.rect(x, y, x2, y2, lcd.BLACK, lcd.BLACK)
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.text(x + 2, y + 2, indicator)
    lcd.font(lcd.FONT_DejaVu40)
    lcd.text(x + (x2 - text_halfwidth), y + 5, text)
    unnotify(note)


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


def draw_cycle(value):
    lcd.rect(160, 0, 160, 50, lcd.BLACK, lcd.BLACK)
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.text(161, 1, "Cycle")
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
    lcd.text(161, 51, "Cn")
    lcd.font(lcd.FONT_DejaVu40)
    lcd.text(int(((320 / 4) * 3) - get_text_halfwidth(value)), 60, str(value))


def draw_ssids(valuelist):
    note = notify("draw ssids")
    max_lenght = 8
    vert_offset = 15
    x = 0
    y = 110
    lcd.font(lcd.FONT_Ubuntu)
    # lcd.setwin(0, 110, 160, 230)
    lcd.rect(0, 105, 320, 130, lcd.BLACK, lcd.BLACK)
    for i, text in enumerate(valuelist):
        if i == max_lenght:
            lcd.rect(160, 105, 160, 115, lcd.BLACK, lcd.BLACK)
            x = 160
            y = 110
        if i == max_lenght * 2:
            break
        text = text[:18] if x else text
        lcd.text(x, y, text)
        y = y + vert_offset
    unnotify(note)


def notify(message):
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.text(160, 220, str(message))
    return message


def unnotify(message):
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.textClear(160, 220, str(message))


def sleep_notice():
    lcd.circle(310, 230, 5, lcd.GREEN, lcd.BLACK)
    time.sleep(5)
    lcd.circle(310, 230, 6, lcd.BLACK, lcd.BLACK)


def csleep(t):
    lcd.circle(310, 230, 5, lcd.GREEN, lcd.BLACK)
    time.sleep(t)
    lcd.circle(310, 230, 6, lcd.BLACK, lcd.BLACK)


def draw_cycles(cycles, undraw=False):
    # prints 'cycles' in 250, 0). Will print if second argument is True
    lcd.font(lcd.FONT_DefaultSmall)
    x, y = 250, 0
    text = "ckl: " + str(cycles)
    if undraw:
        lcd.textClear(x, y, text)
    else:
        lcd.text(x, y, text)


# ========================= FS stuff ========================================


def load_json(filename):
    filename = filename
    note = notify("reading " + filename)
    content = {}
    try:
        with open(filename) as f:
            content = json.load(f)
            unnotify(note)
    except Exception:
        note = notify("unavailable. making new")
        write_json(filename, content)
        unnotify(note)
    return content


def write_json(filename, content):
    # note = notify("saving")
    try:
        with open(filename, "w+") as f:
            json.dump(content, f)
    except Exception:
        # notify = notify("failed to save")
        time.sleep(1)
        # unnotify(note)
    # unnotify(note)
