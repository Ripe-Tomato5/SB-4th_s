import base64
import lora
import serial
import sys
import time
import numpy as np

lr = lora.LoRa()

def sendcmd(cmd):
    print(cmd)
    lr.write(cmd)
    t = time.time()
    while (True):
        if (time.time() - t) > 5:
            print('panic: %s' % cmd)
            break
        line = lr.readline()
        if 'OK' in line:
            print(line)
            return True
        elif 'NG' in line:
            print(line)
            return False

def start():
    lr.reset()
    time.sleep(1.5)

    line = lr.readline()
    while not ('Mode' in line):
        lr.reset()
        line = lr.readline()
        if len(line) > 0:
            print(line)
        time.sleep(0.5)
    sendcmd('2\r\n')
    time.sleep(0.5)
    sendcmd('start\r\n')
    print("LoRa started Picture transmission is ready!!")

def main():
    try:
        start()
        time.sleep(5)
        while True:
            line = lr.readline()
            binary_data = binary_data + base64.b64decode(line)
            

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        with open("output.jpg", "wb") as f:
            f.write(binary_data)
        print("Base64データをバイナリに変換して output.jpg として保存しました。")
        print("長さ:", len(binary_data))
        print("先頭100文字:\n", binary_data[:5848])  # 一部だけ表示
        lr.close()

if __name__ == "__main__":
    main()

