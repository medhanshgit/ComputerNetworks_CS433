import socket
import cip
import os
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
s = socket.socket()        
print ("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345               
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
# print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
# accept connection if there is any
client_socket, address = s.accept() 
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")
# receive the file infos
# receive using client socket, not server socket
req = client_socket.recv(1024).decode()

while req != "exit":
##UPLOAD--------------------------------------------------------------------------------------------------
    if req == "UPD":
        filename = client_socket.recv(1024).decode()
        e = client_socket.recv(1024).decode()
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # start receiving the file from the socket
        # and writing to the file
        with open(filename, "wb") as f:
            while True:
                # read bytes from the socket (receive)
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    print("Received")
                    break
                print("Receiving")
                # write to the file the bytes we just received
                f.write(bytes_read)
        cip.decrypt(e,filename)
        break

##DOWNLOAD-----------------------------------------------------------------------------------------------
    if req == "DWD":
        filename = client_socket.recv(1024).decode()
        e = client_socket.recv(1024).decode()
        # remove absolute path if there is
        filename = os.path.basename(filename)
         # start sending the file
        cip.encrypt(e,filename)
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    print("Sent")
                    client_socket.shutdown(socket.SHUT_WR)
                    break
                client_socket.send(bytes_read)
                print("Sending")
        cip.decrypt(e,filename)
        break


##CURRENT DIR---------------------------------------------------------------------------------------------
    if req == "CWD":
        dir = os.getcwd()
        client_socket.send(dir.encode())

##LIST DIR-----------------------------------------------------------------------------------------------
    if req == "LS":
        path = os.getcwd()
        dir = os.listdir(path)
        client_socket.send(format(dir).encode())

##CHANGE DIR---------------------------------------------------------------------------------------------
    if req == "CD":
        path = os.getcwd()
        client_socket.send(format(path).encode())
        dir = client_socket.recv(1024).decode()
        os.chdir(format(dir))
        path = os.getcwd()
        client_socket.send(format(path).encode())
    
##NEXT req-----------------------------------------------------------------------------------------------
    req = client_socket.recv(1024).decode()

client_socket.close()
s.close()