import socket
import sys



print("Do Ctrl+c to exit the program !!")

def EnvoiUDP(data:str,IP:str,PORT:int):

    datasend:str=data
    # Create socket for server
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(bytes(datasend, "utf-8"), (IP, PORT))

    # close the socket
    s.close()

