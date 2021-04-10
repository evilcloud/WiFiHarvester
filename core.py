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


# printing functions
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
    lcd.line(5, 103, 320, 103)
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.text(245, 55, "SC")
    lcd.text(245, 70, "SV")
    lcd.text(245, 85, "FU")


# quadrant functions: large quadrants


# def text_halfwidth(text):
#     return int(lcd.textWidth(str(text)) / 2)


def draw_quadrants(position, vector, fonts, legend, value):
    text_halfwidth = lambda text: int(lcd.textWidth(text) / 2)
    x, y = position
    x1, y1 = vector
    font_small, font_large = fonts
    value = str(value)
    lcd.rect(x + 1, y + 1, x1 - 1, y1 - 1, lcd.BLACK, lcd.BLACK)
    lcd.font(font_small)
    lcd.text(x + 1, y + 1, legend)
    lcd.font(font_large)
    middle_x = int(x + (x1 / 2) - text_halfwidth(value))
    lcd.text(middle_x, y + 1, value)


# big quadrants
def big_quadrant(position, legend, value):
    draw_quadrants(
        position, (160, 50), (lcd.FONT_DefaultSmall, lcd.FONT_DejaVu40), legend, value
    )


def draw_ap(value):
    big_quadrant((0, 0), "AP", value)


def draw_ssid(value):
    big_quadrant((160, 0), "SSID", value)


def draw_cfamiliar(value):
    third_quadrant((0, 50), "Cf", value)


def draw_cnew(value):
    third_quadrant((120, 50), "Cn", value)


# one third quadrant
def third_quadrant(position, legend, value):
    draw_quadrants(
        position, (120, 50), (lcd.FONT_DefaultSmall, lcd.FONT_DejaVu40), legend, value
    )


# quadrant functions: top-right info quadrant
def draw_cycle(value):
    draw_quadrants(
        (240, 0), (80, 25), (lcd.FONT_DefaultSmall, lcd.FONT_DejaVu18), "Cy", value
    )


def draw_bssid_loop(value):
    draw_quadrants(
        (160, 0), (80, 25), (lcd.FONT_DefaultSmall, lcd.FONT_DejaVu18), "", value
    )


# indicator dots
def draw_dot(y_position, legend, color):
    positions = {
        "SC": 60,
        "SV": 75,
        "FU": 90,
    }
    lcd.circle(300, positions.get(legend), 5, lcd.GREEN, color)


def draw_dot_scan(value):
    values = {
        "black": lcd.BLACK,
        "yellow": lcd.YELLOW,
        "green": lcd.GREEN,
        "red": lcd.RED,
    }
    draw_dot(60, "SC", values.get(value))


def draw_dot_save(value):
    values = {
        "black": lcd.BLACK,
        "yellow": lcd.YELLOW,
        "green": lcd.GREEN,
        "red": lcd.RED,
    }
    draw_dot(75, "SV", values.get(value))


def draw_dot_fu(value):
    values = {
        "black": lcd.BLACK,
        "yellow": lcd.YELLOW,
        "green": lcd.GREEN,
        "red": lcd.RED,
    }
    draw_dot(90, "FU", values.get(value))


def draw_status(text):
    lcd.rect(161, 25, 159, 23, lcd.BLACK, lcd.BLACK)
    lcd.font(lcd.FONT_Ubuntu)
    lcd.text(161, 30, text)


def reset_progress_bar():
    lcd.rect(160, 24, 340, 24, lcd.BLACK, lcd.BLACK)


def draw_progress_line(value):
    lcd.line(161, 24, 160 / value, 24)


# non-quadrant ssid listing


def draw_ssids(valuelist):
    note = notify("draw ssids")
    max_lenght = 8
    vert_offset = 15
    x = 0
    y = 110
    lcd.font(lcd.FONT_Ubuntu)
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


# notifications drawing


def circle():
    lcd.circle(310, 230, 5, lcd.RED, lcd.RED)


def uncircle():
    lcd.cirle(310, 230, 6, lcd.BLACK, lcd.BLACK)


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


# ========================= FS stuff ========================================


def load_json(filename):
    filename = filename
    content = {}
    try:
        with open(filename) as f:
            content = json.load(f)
            message = "loaded " + str(len(content)) + " entries"
    except Exception:
        message = "unavailable. making new"
        write_json(filename, content)
    return content, message


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


def add(filename, data):
    try:
        with open(filename, "a") as f:
            f.write(data)
        err = False
    except Exception as e:
        err = str(e)
    return err


def count_entries(filename):
    counter = 0
    try:
        with open(filename) as f:
            full_file = f.read()
        for line in full_file:
            if line[:2] == "===":
                counter += 1
    except Exception:
        pass
    return counter