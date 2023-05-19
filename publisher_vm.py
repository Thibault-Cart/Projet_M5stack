import socket
import paho.mqtt.client as mqtt
import time

TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
#ip Publisher
TCPServerSocket.bind(("192.168.27.248",1234))
TCPServerSocket.listen(2)
i = 0
while i <= 20:
    print("Le serveur TCP attend une co")
    connexion, addr =  TCPServerSocket.accept()

    msgClient = connexion.recv(1024).decode("UTF-8")
    print("Message m5Stack :", msgClient)

    mqttclient=mqtt.Client("publisher")
	#Ip Brocker
    mqttclient.connect("192.168.27.183")
    if msgClient == "aimant" or msgClient == "pas aimant":
    	mqttclient.publish("Aimant", msgClient)
    else:
        mqttclient.publish("temperature", msgClient)
    mqttclient.loop(2)

    time.sleep(1)
    #i+=1
    connexion.close()
TCPServerSocket.close()
