import serial

ser = serial.Serial("/dev/serial0", 115200, timeout=1)

while True:
    data = ser.read(100)  # 読み取り
    if data:
        print("受信:", data)
