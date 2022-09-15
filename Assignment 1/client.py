import socket
import cip
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step
# the ip address or hostname of the server, the receiver
host = "127.0.0.1"
# the port, let's use 5001
port = 12345
# the name of file we want to send, make sure it exists

# create the client socket
s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")
# send the filename and filesize
req = input("enter command:")
if req == "CWD" or req == "LS" or req == "exit":
    breq = req.encode()
    s.send(breq)
else:
    req, file = req.split()
    breq = req.encode()
    s.send(breq)

while req != "exit":
##UPLOAD--------------------------------------------------------------------------------------------------
    if req == "UPD":
        filename = file
        e = input("which encryption out of (plaintext,substitution,transpose):")
        s.send(filename.encode())
        cip.encrypt(e,filename)
        s.send(e.encode())
        # start sending the file
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    print("Sent")
                    s.shutdown(socket.SHUT_WR)
                    break
                s.send(bytes_read)
                print("Sending")
        cip.decrypt(e,filename)
        break

##DOWNLOAD-----------------------------------------------------------------------------------------------
    if req == "DWD":
        filename = file
        e = input("which encryption out of (plaintext,substitution,transpose):")
        s.send(filename.encode())
        s.send(e.encode())
        # start writing to the file
        with open(filename, "wb") as f:
            while True:
                # read bytes from the socket (receive)
                bytes_read = s.recv(BUFFER_SIZE)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    print("Received")
                    break
                # write to the file the bytes we just received
                print("Receiving")
                f.write(bytes_read)
        cip.decrypt(filename, e)
        break

##CURRENT DIR---------------------------------------------------------------------------------------------
    if req == "CWD":
        dir = s.recv(1024).decode()
        print(dir)

##LIST DIR-----------------------------------------------------------------------------------------------
    if req == "LS":
        dir = s.recv(1024).decode()
        print(dir)

##CHANGE DIR---------------------------------------------------------------------------------------------
    if req == "CD":
        path = s.recv(1024).decode()
        print("Initial directory:",path)
        s.send(file.encode())
        path = s.recv(1024).decode()
        print("Current directory:",path)

##NEXT req-----------------------------------------------------------------------------------------------
    req = input("enter command:")
    if req == "CWD" or req == "LS" or req == "exit":
        breq = req.encode()
        s.send(breq)
    else:
        req, file = req.split()
        breq = req.encode()
        s.send(breq)

s.close()