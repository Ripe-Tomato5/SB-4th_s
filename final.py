from picamera2 import Picamera2
import base64
import lora
import serial
import sys
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import Murata

lr = lora.LoRa()
mr = Murata.murata()
# カメラ初期化
picam2 = Picamera2()

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

def Murapic():
    # カメラの準備（構成）
    conf = picam2.create_preview_configuration(main = {"size": (640, 480)})
    picam2.configure(conf)
    picam2.start()
    # カメラ起動待ち（2秒程度）
    time.sleep(2)
    # 画像を保存（JPEG形式）
    Picture_name = "MurataPicture.jpg"
    picam2.capture_file(Picture_name)
    picam2.stop()
    print(f"画像を {Picture_name} として保存しました。")
    input_img = cv2.imread(f"{Picture_name}")
    # 画像を180度回転して上書き保存
    output_img = cv2.rotate(input_img, cv2.ROTATE_180)
    cv2.imwrite(f"{Picture_name}", output_img)

def cam_reduce():
    mr.posterize_main("MurataPicture.jpg") # 画像のポスタライズ化
    mr.size_reduce("Artistic_Murata.jpg") # 画像のサイズを削減

def royal():  
    # カメラの準備（構成）高画素モード
    conf = picam2.create_preview_configuration(main = {"size": (2592, 1944)})
    picam2.configure(conf)
    picam2.start()
    # カメラ起動待ち（2秒程度）
    time.sleep(2)
    # 画像を保存（JPEG形式）
    Picture_name = "MurataPicture_Royal.jpg"
    picam2.capture_file(Picture_name)
    picam2.stop()
    print(f"画像を {Picture_name} として保存しました。")
    input_img = cv2.imread(f"{Picture_name}")
    # 画像を180度回転して上書き保存
    output_img = cv2.rotate(input_img, cv2.ROTATE_180)
    cv2.imwrite(f"{Picture_name}", output_img) 

# JPEGをバイナリで読み込み
def jpg_send(Picture_name):
    with open(f"{Picture_name}", "rb") as f:
        binary_data = f.read()
    print("original_data_size:", len(binary_data), "bytes")
    #Base64でASCII文字列に変換
    ascii_data = base64.b64encode(binary_data).decode("ascii")
    print("ascii_data size:", len(ascii_data), "bytes")
    chunk_size = 48
    total_chunks = (len(ascii_data) + chunk_size - 1) // chunk_size
    for i in range(0, len(ascii_data), chunk_size):
        chunk = ascii_data[i:i + chunk_size]
        payload = chunk + "\r\n"
        sendcmd(payload)
        print(f"Sent chunk {i // chunk_size + 1} / {total_chunks}")
        print(ascii_data[i:i + chunk_size])
        time.sleep(3)  # 送信間隔を調整

def camstop():
    picam2.close()

def main():

    try:
        start()
        time.sleep(5)
        royal()
        Murapic()
        camstop()
        cam_reduce()
        jpg_send("Artistic_Murata.jpg")
  
    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        lr.close()

if __name__ == "__main__":
    main()
