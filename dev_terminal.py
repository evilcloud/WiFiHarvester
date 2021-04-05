import json
import time
import os


def init():
    print("launching WiFiHarvester 3.2\nin terminal\n")


def cclear(color=lcd.BLACK):
    pass


def cprint(*args):
    lprint(" ".join([str(i) for i in args]))


def cprintln(*args):
    cprint(*args)
    print("\n")


def draw_grid():
    pass


def draw_indicators(indicator, value):
    print(indicator, value)


def get_text_halfwidth(text):
    pass


def draw_ap(value):
    print(f"AP: {value}")


def draw_ssid(value):
    print(f"SSID: {value}")


def draw_cfamiliar(value):
    print(f"CF: {value}")


def draw_cnew(value):
    print(f"CNew: {value}")


def draw_ssids(valuelist):
    for i in valuelist:
        print(f"   {i}")


def notify(message):
    pass


def unnotify(message):
    pass


def sleep_notice():
    pass


def csleep(t):
    pass


def draw_cycles(cycles, undraw=False):
    pass


# ========================= FS stuff ========================================


def load_json(filename):
    content = {}
    try:
        note = notify("reading " + filename)
        with open(filename) as f:
            content = json.load(f)
            unnotify(note)
    except Exception:
        note = notify("unavailable. making new")
        write_json(filename, content)
        unnotify(note)
    return content


def write_json(filename, content):
    note = notify("saving")
    try:
        with open(filename, "w+") as f:
            json.dump(content, f)
    except Exception:
        notify = notify("failed to save")
        time.sleep(1)
        unnotify(note)
    unnotify(note)
