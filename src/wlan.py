import network
import time
import os

def connect_sta(ssid, key, timeout=5):
    wlan = None
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    wlan.connect(ssid, key)
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < timeout * 1000:
        time.sleep_ms(500)
        if wlan.isconnected():
            break
    if not wlan.isconnected():
        wlan.active(False)
        wlan = None
    return wlan

def connect_ap():
    wlan = network.WLAN(network.AP_IF)
    wlan.active(True)
    wlan.config(authmode=network.AUTH_WPA2_PSK)
    wlan.config(essid="WatchNet", password="NeverGonaGive")
    wlan.config(max_clients=4)
    return wlan

def connect_wlan(timeout=5):
    wlan = None
    if "wlan_credentials.py" in os.listdir():
        from wlan_credentials import SSID, PASS
        disconnect_wlan()
        wlan = connect_sta(SSID, PASS, timeout)
    if not wlan:
        disconnect_wlan()
        wlan = connect_ap()
    return wlan

def disconnect_wlan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan = network.WLAN(network.AP_IF)
    wlan.active(False)
