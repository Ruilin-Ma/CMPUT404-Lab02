#!/usr/bin/env python3
import socket
import time
import sys
from multiprocessing import Process

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
        # reuse the same port 
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
                
                
                #continuously listen for connections
                while True:
                    conn, addr = proxyEnd.accept()
                    p = Process(target=handle_proxy, args = (addr, conn))
                    p.daemon = True
                    p.start()
                    print("Started process ", p)
            #     data= proxyEnd.recv(BUFFER_SIZE)
            #     print(f"Sending received data {data} to client")
            #     conn.send(data)
                
            conn.close()

def handle_proxy(addr, conn):
    print("Connected by", addr)
    #recieve data, wait a bit, then send it back
    
    full_data = conn.recv(BUFFER_SIZE)
    print (f"Sending received data {full_data} to google")
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)

    data= conn.recv(BUFFER_SIZE)
    print(f"Sending received data {data} to client")
    conn.send(data)


if __name__ == "__main__":
    main()