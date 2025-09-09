from picamera2 import Picamera2
import time

# カメラ初期化
picam2 = Picamera2()

# カメラの準備（構成）
picam2.configure(picam2.create_still_configuration())

# カメラ起動
picam2.start()

# カメラ起動待ち（2秒程度）
time.sleep(2)

# 画像を保存（JPEG形式）
picam2.capture_file("photo.jpg")

print("画像を photo.jpg として保存しました。")