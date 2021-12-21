# cliente.py
import socket
import json
from app import App

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get a local machine name
# IP server
host = '127.0.0.1'
# Server PORT
port = 9999

# connection to hostname on the port
s.connect((host, port))

# create a App object
clientApp = App()

# collecting user data
values = clientApp.collectUserData()

# processing user data
listData = clientApp.validateData(values)
finalData = clientApp.generateDict(listData)

# serialising data
# pass the data to json
data = json.dumps(finalData)

# pass to bytes
data = data.encode("ascii")

# send data to server
s.send(data)

# recive no more than 1024 bytes
# pass to json
response = s.recv(1024).decode()

# pass to dict
response = json.loads(response)

# menu
clientApp.menu(response)

# close connection
s.close()