from machine import Pin
from time import sleep
import socket
import network
import time
from m5stack import lcd

AUTH_OPEN = 0
AUTH_WEP = 1
AUTH_WPA_PSK = 2
AUTH_WPA2_PSK = 3
AUTH_WPA_WPA2_PSK = 4

SSID = "Sam"
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
    
    
IP = "192.168.27.176" # Remplacer par l'adresse IP de votre serveur UDP sur Packet Tracer
PORT = 1235 # Remplacer par le port utilisé par votre serveur UDP sur Packet Tracer
 
class Pir():
    def __init__(self):
        self.pin = Pin(22,Pin.IN)
        self.pin.irq(trigger=(Pin.IRQ_RISING | Pin.IRQ_FALLING),
                     handler=self.actionInterruption)
        print("Début du test de présence")
    
    def actionInterruption(self,pin):
        UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if (self.pin.value()==1):
            lcd.clear(lcd.CYAN)
            lcd.setCursor(80,80)
            print("Presence detecté")
            lcd.print("Presence dans IRM")
            message = "1"
            UDPClientSocket.sendto(message, (IP, PORT))
        else:
            lcd.clear(lcd.PURPLE)
            lcd.setCursor(80,80)
            print("Personne est présent")
            lcd.print("RAS")
            message = "0"
            UDPClientSocket.sendto(message, (IP, PORT))
        UDPClientSocket.close()

p=Pir()
connect()
while True:
    sleep(0.5)
