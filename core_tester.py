import core as dev

dev.cclear()
dev.dev.draw_ap(9999)
dev.draw_ssid(9999)
dev.draw_cfamiliar(9999)
dev.draw_cnew(9999)
dev.notify("something")
dev.draw_ssids(
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
dev.unnotify("something")
dev.sleep_notice()
