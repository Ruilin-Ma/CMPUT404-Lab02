#!/usr/bin/env python3
import socket
import time
import sys

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024
def getIP (host):
    print ("Getting IP for ", host)
    try: 
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print ("Hostname could not be resolved, Existing")
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip
def main():
    host = 'www.google.com'
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxyStart:
        print("Starting proxy server")
        #QUESTION 3
        proxyStart.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        proxyStart.bind((HOST, PORT))
        #set to listening mode
        proxyStart.listen(1)
        
        #continuously listen for connections
        while True:
            conn, addr = proxyStart.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxyEnd:
                print("Connecting to Google")
                remote_ip = getIP(host)
                
                proxyEnd.connect((remote_ip, port))
                #recieve data, wait a bit, then send it back
                send_full_data = conn.recv(BUFFER_SIZE)
                print (f"Sending received data {send_full_data} to google")
                proxyEnd.sendall(send_full_data)
                proxyEnd.shutdown(socket.SHUT_WR)

                data= proxyEnd.recv(BUFFER_SIZE)
                print(f"Sending received data {data} to client")
                conn.send(data)
                
            conn.close()

if __name__ == "__main__":
    main()
