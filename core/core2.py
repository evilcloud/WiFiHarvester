from m5stack import *
import utime as time
import wifiscanbase


# Launch sequence
devid = wifiscanbase.get_devid("M5Core2")
masterlist_bssid = wifiscanbase.read_json("/sd/stations.json")

power.setPowerLED(False)
lcd.font(lcd.FONT_DejaVu18)
lcd.clear()
lcd.setCursor(10, 10)
lcd.print("Launching WiFi scanner\n")
lcd.print("DevID: " + devid + "\n")
lcd.print("\nHarvested to date:\n")
lcd.print("Individual AP: " + len(masterlist_bssid) + "\n")
lcd.print("Unique SSID:  " + str(len(wifiscanbase.get_unique_ssid(masterlist_bssid))))


bssid_file = '/sd/stations.json'
while True:
    