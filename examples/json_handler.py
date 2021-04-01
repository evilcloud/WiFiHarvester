#!/usr/bin/python3

import json
import sys
import os


def get_data(filename, sbssids):

    with open(filename) as f:
        jcontent = json.load(f)

    ssid = []
    bssid = []
    cnt = []
    hidden = []
    devid = []
    channel = []
    authmode = []

    print(f"Total entries: {len(jcontent)}")
    for item in jcontent:
        entries = jcontent[item]
        ssid.append(entries["ssid"])
        bssid.append(entries["bssid"])
        cnt.append(entries["count"])
        hidden.append(entries["hidden"])
        devid.append(entries["devID"])
        channel.append(entries["channel"])
        authmode.append(entries["authmode"])

    if len(set(jcontent)) == len(jcontent):
        print("all unique entries")
    else:
        print(
            f"somehow there are {len(jcontent) - len(set(jcontent))} duplicates. Investigate!"
        )
    print(f"of which {hidden.count(True)} entries are hidden")
    print(f"largest count is {max(cnt)}")
    udevid = set(devid)
    print(f"there are {len(udevid)} unique devices: {udevid}")
    if sbssids:
        for s_station in sbssids:
            print(
                f"similarities with {s_station[0]}: {len(set(s_station[1]) & set(bssid))}"
            )
    return bssid


filename = ""
sbssids = []
directory = "station_jsons/"
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filelist = [
        directory + file for file in os.listdir(directory) if file.endswith(".json")
    ]
    if not filelist:

        print("nothing found. bye")
        sys.exit(0)
    print(f"found {len(filelist)} stations:")
    print(filelist)
    for station in filelist:
        print("\n----------------")
        print(f"\nopening {station}")
        sbssids.append((station, get_data(station, sbssids)))
    print("done")
