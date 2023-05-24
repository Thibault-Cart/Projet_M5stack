import network
import time
import socket


SSID = "SSID"
PASSWORD = "PASSWORD"

def do_connect(ssid,psw):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    s = wlan.config("mac")
    mac = ('%02x:%02x:%02x:%02x:%02x:%02x').upper() %(s[0],s[1],s[2],s[3],s[4],s[5])
    print("Local MAC:"+mac) #get mac 
    wlan.connect(ssid, psw)
    if not wlan.isconnected():
        print('connexion au reseau...' + ssid)
        wlan.connect(ssid, psw)
 
    start = time.ticks_ms() # get millisecond counter
    while not wlan.isconnected():
        time.sleep(1) # sleep for 1 second
        if time.ticks_ms()-start > 20000:
            print("Timeout de connexion!")
            break
 
    if wlan.isconnected():
        print('Adresses IP:', wlan.ifconfig())
    return wlan
 
def connect():
 do_connect(SSID,PASSWORD)
 



