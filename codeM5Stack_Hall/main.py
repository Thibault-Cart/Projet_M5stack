from machine import Pin
from time import sleep
from m5stack import lcd
import socket
import wifiConnection


#ip du m5stack "192.168.105.51"

# machine d'état pour savoir quand valeur capteur change
Anc_EtatCapteurHall=""
EtatCapteurHall=""

# constantes pour comunication TCP
PORT = 1234
IP_PUBLISHER = "192.168.27.248"

# class permantant la lecture du capteur HALL
class Hall():
     def __init__(self):
         self.pin = Pin(22,Pin.IN)
         self.pin.irq(trigger=(Pin.IRQ_RISING | Pin.IRQ_FALLING),
             handler=self.actionInterruption)
     def actionInterruption(self,pin):
         global Anc_EtatCapteurHall,EtatCapteurHall
         if (pin.value()==1):
             Anc_EtatCapteurHall=EtatCapteurHall
             EtatCapteurHall="pas aimant"
         else:
             Anc_EtatCapteurHall=EtatCapteurHall
             EtatCapteurHall="aimant"
             


def main():
    global Anc_EtatCapteurHall,EtatCapteurHall,IP_PUBLISHER,PORT
    
    # appel la fonction connect du fichier wifiConnection.py
    wifiConnection.connect()
    # instantiation Hall
    h=Hall()
    
    socketTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    print("connecter")
    
    while(True):
        # s ichangement d'état du capteur
        if(Anc_EtatCapteurHall!=EtatCapteurHall):
        #creation socket
            socketTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #connection socket
            socketTcp.connect((IP_PUBLISHER, PORT))
            print(EtatCapteurHall)
            #envoie data au publisher
            socketTcp.send((EtatCapteurHall).encode("UTF-8"))
            # Recevoir la réponse du serveur
            response = socketTcp.recv(1024)  # Taille du tampon : 1024 octets
            print("Réponse du serveur :", response.decode())
            Anc_EtatCapteurHall=""
            EtatCapteurHall=""
            socketTcp.close()
        sleep(1)
    
if __name__ == "__main__":
    
    main()


            
            
            
        







