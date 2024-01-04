import socket
import time
import cv2
import numpy as np
from utils.utils import recvFile

import keyboard
import requests

url = "mahasahakar.in/Odysseus"
r = requests.get(url)
HOST = r.json()["ip"]
PORT = r.json()["port"]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

if s.recv(1024).decode("utf-8") == "connected":
    print("Connected to server")
else:
    print("Failed to connect to server")
    exit()

# Menu
print("Select mode:")
print("1. Teleop")
print("2. Map Static Environment")
mode = input("Enter mode: ")
s.sendall(mode.encode("utf-8"))

if mode == "1":
    while True:
        time.sleep(0.05)                    # Watch out! can cause lag
        if keyboard.is_pressed("up arrow"):
            s.sendall(b"w")
        elif keyboard.is_pressed("down arrow"):
            s.sendall(b"s")
        elif keyboard.is_pressed("left arrow"):
            s.sendall(b"a")
        elif keyboard.is_pressed("right arrow"):
            s.sendall(b"d")
        elif keyboard.is_pressed("space"):
            s.sendall(b"img")
            while True:
                data = s.recv(1024)
                if data == b"done":
                    break
                img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), -1)
                cv2.imshow("Image", img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        elif keyboard.is_pressed("q"):
            s.sendall(b"q")
            break
        else:
            pass

elif mode == "2":
    recvFile(s, "staticMap.jpg")
    print("Map saved as staticMap.jpg")

s.shutdown(2)
s.close()
