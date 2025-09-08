import serial
import time

ser = serial.Serial("/dev/serial0", 115200, timeout=1)

while True:
    payload = b"HELLO"
    ser.write(payload)   # そのまま送信
    print("送信:", payload)
    time.sleep(2)
