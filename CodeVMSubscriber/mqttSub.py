import paho.mqtt.client as mqtt #import the client1
import time
import keyboard
import udpSend
import socket

def on_message(client, userdata, message):
    IP="192.168.27.176"
    PORT=1236
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    userdata=(str(message.payload.decode("utf-8")))
    udpSend.EnvoiUDP(userdata,IP,PORT)

broker_address="192.168.27.183"
TOPIC_1="temperature"
TOPIC_2="Aimant"

print("creation de la nouvelle instance")
client = mqtt.Client("client1")
client.on_message=on_message
print("connection au broker")
client.connect(broker_address)
client.loop_start() #démarrage de la boucle
print("Inscription au topic")
client.subscribe(TOPIC_1)
client.subscribe(TOPIC_2)
fin = False
while fin == False:
    if keyboard.is_pressed('q'):
        print('On a fini!')
        fin = True

client.loop_stop()
