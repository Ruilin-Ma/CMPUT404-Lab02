import socket
from multiprocessing import Process

HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024
payload = f"GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n"

def connect(addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        s.sendall(payload.encode())
        s.shutdown(socket.SHUT_WR)

        full_data = s.recv(BUFFER_SIZE)
        print('full_data is: ', full_data)

    except Exception as e:
        print (e)
    finally:
        s.close()

def main():
    addr=HOST
    conn=PORT
    for i in range (5):
        p = Process(target=connect, args = ((addr, conn),))
        print("Started process ", p)
        p.daemon = True
        p.start()
        p.join()
    
    

if __name__ == "__main__":
    main()