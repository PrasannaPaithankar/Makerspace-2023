import cv2


def captureImg():
    """Captures an image from the camera and returns it as a numpy array"""
    cap = cv2.VideoCapture(0)
    _, img = cap.read()
    cap.release()
    cv2.imwrite("./tmp/img.jpg", img)
    return "./tmp/img.jpg"


def sendFile(s, path):
    """Sends a file to the client"""
    file = open(path, "rb")
    data = file.read(1024)
    while data:
        s.send(data)
        data = file.read(1024)
    file.close()
    print("Done Sending")
    s.sendall(b"done")


def recvFile(s, path):
    """Receives a file from the client"""
    file = open(path, "wb")
    while True:
        data = s.recv(1024)
        if data == b"done":
            break
        file.write(data)
    file.close()
    print("Done Receiving")
    return path
