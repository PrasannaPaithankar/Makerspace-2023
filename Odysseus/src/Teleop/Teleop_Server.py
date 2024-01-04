import socket

import requests
from LiDAR.LiDAR import genStaticMap
from Motors import Motors
from utils.utils import captureImage, sendFile

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65000

url = "mahasahakar.in/Odysseus"
r = requests.post(url, data={"ip": HOST, "port": PORT})

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()

print(f"Connected to Controller: {addr}")
s.sendall(b"connected")

motors = Motors([17, 18], [22, 23], [24, 25], [5, 6])
motors.test()

mode = conn.recv(1024).decode("utf-8")

if mode == "1":
    print("Teleop Mode")
    while True:
        data = conn.recv(1024).decode("utf-8")
        if data == "w":
            motors.forward(0.5)
        elif data == "s":
            motors.backward(0.5)
        elif data == "a":
            motors.left(0.5)
        elif data == "d":
            motors.right(0.5)
        elif data == "img":
            motors.stop()
            imgPath = captureImage()
            sendFile(conn, imgPath)
        elif data == "q":
            motors.stop()
            break
        else:
            motors.stop()

elif mode == "2":
    print("Map Static Environment Mode")
    mapPath = genStaticMap()
    sendFile(conn, mapPath)

conn.shutdown(2)
conn.close()
s.shutdown(2)
s.close()
