# https://sozorablog.com/camera_shooting/
# OpenCVライブラリを使って画像を保存

# OpenCVライブラリをインストール、numpyモジュールをインストール、パッケージリストを最新に
# sudo pip3 install opencv-python
# pip install numpy
# sudo apt update

# imageフォルダをマイコンに作成（していなければ）
# mkdir SB-4th_s/image

import cv2
import os

cap = cv2.videoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

i = 1
j = 0

if altitude == 30: #条件を満たすと1度に3回写真を撮る、上空10kmで写真を撮る、（何十分間で間隔を開けて写真を撮る機能も実装したい）ここではaltitude変数を仮でおいている
  for j in range(3):
    ret, frame = cap.read()
    path = 'SB-4th_s/Images'
    cv2.imwrite(os.path.join(path,'take_' + str(i) + '.jpg'), frame) #Imagesファイルに画像を保存,https://ja.python-3.com/?p=23318
    cap.release()
    i = i + 1