from picamera2 import Picamera2
import time
import base64
import cv2

# カメラ初期化
picam2 = Picamera2()
# カメラの準備（構成）
picam2.configure(picam2.create_still_configuration())
# カメラ起動
picam2.start()

# カメラ起動待ち（2秒程度）
time.sleep(2)

# 画像を保存（JPEG形式）
Picture_name = "MurataPicture.jpg"
picam2.capture_file(Picture_name)
print(f"画像を {Picture_name} として保存しました。")
input_img = cv2.imread(f"/home/SB-4th_s/{Picture_name}")
# 画像を180度回転して上書き保存
output_img = cv2.rotate(input_img, cv2.ROTATE_180)
cv2.imwrite(f"/home/SB-4th_s/{Picture_name}", output_img)

# JPEGをバイナリで読み込み 
with open(f"/home/SB-4th_s/{Picture_name}", "rb") as f:
    binary_data = f.read()
print("original_data_size:", len(binary_data), "bytes")

#Base64でASCII文字列に変換
ascii_data = base64.b64encode(binary_data).decode("ascii")
print("ascii_data size:", len(ascii_data), "bytes")
