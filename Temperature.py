import network
import machine
from machine import I2C, Pin
import time
from m5stack import *
import socket

AUTH_OPEN = 0
AUTH_WEP = 1
AUTH_WPA_PSK = 2
AUTH_WPA2_PSK = 3
AUTH_WPA_WPA2_PSK = 4

SSID = ""
PASSWORD = ""

 
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


class SHT30:
    def __init__(self, scl_pin=22, sda_pin=21, i2c_address=0x44):
        self.i2c = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.i2c_addr = i2c_address
        time.sleep_ms(50)
    def measure(self):
        self.i2c.writeto(self.i2c_addr, '\x2C\x10')
        time.sleep_ms(200)
        data = self.i2c.readfrom(self.i2c_addr, 6)
        temp = (((data[0] << 8 | data[1]) * 175.0) / 65535) - 45
        humi = (((data[3] << 8 | data[4]) * 100.0) / 65535)
        return temp
    
c=SHT30()

PORT = 1234
IP_PUBLISHER = "192.168.27.248"

#Connexion au réseau
connect()
while True:
    print(c.i2c.scan())
    # Initialisation de la socket TCP
    TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connexion au publisher MQTT
    TCPClientSocket.connect((IP_PUBLISHER, PORT))
    #Récupération de la température (2 décimales)
    temp = str(round(c.measure(), 2))
    if(c.measure() > 28.0):
        lcd.clear(0x0000FF)
        lcd.text(0, 0, "Température trop haute " + str(temp) + "°")
    else:
        lcd.clear(0xFF0000)
        lcd.text(0, 0, "Température convenable " + str(temp) + "°")
    TCPClientSocket.sendall(str(temp).encode("UTF-8"))
    time.sleep(7)
    TCPClientSocket.close()
TCPClientSocket.send(b"")
TCPClientSocket.close()
