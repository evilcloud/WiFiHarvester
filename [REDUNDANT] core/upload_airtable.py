import json
import requests
import os


def upload_data(station):
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

        url = "https://v1.nocodeapi.com/evilcloud/airtable/ftxgIWRLzYIHPsBV?tableName=stations"
        params = {}
        
        data = [{"bssid":entries["bssid"], "ssid":entries["ssid"], "count":entries["count"], "hidden":entries["hidden"],"devID":entries["devID"], "channel":entries["channel"], "authmode":entries["authmode"]}]
        r = requests.post(url = url, params = params, json = data)
        result = r.json()
        print(result)




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
        answ = input(station)
        if answ == "":
            upload(station)
        else:
            print(f'skipping {station}')
