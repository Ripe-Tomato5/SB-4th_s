# https://invisiblepotato.com/google-colaboratory01/#vnc-viewer%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB-pc%E6%93%8D%E4%BD%9C

from PIL import Image
from IPython.display import display

# 画像を読み込む
img = Image.open("画像ファイル名")

# OpenCVを利用し画質を削減，品質(quality)=20に設定
# https://tat-pytone.hatenablog.com/entry/2021/04/25/114334
import cv2

im = cv2.imread('ファイル.jpg') #できればフルパスで
name = "ファイル"
cv2.imwrite(name + 'reduced.jpg', im, [int(cv2.IMWRITE_JPEG_QUALITY), 20])

# 画像を表示
# display(img)

# jpegファイルをバイナリデータに変換、バイナリファイルを出力するプログラム
# https://elsammit-beginnerblg.hatenablog.com/entry/2020/12/08/232627

import os
import io
from PIL import Image
import numpy as np
import pathlib

#圧縮前画像が入っているファイルの中をすべて参照
# https://zenn.dev/k_neko3/articles/8b89b0ab1c29f8

input_dir = "SB-4th_s/image" # 画像ファイルパス
input_list = list(pathlib.Path(input_dir).glob('**/*.jpg'))

for i in range(len(input_list)):
   img_file_name = str(input_list[i])
   img_np = np.fromfile(img_file_name, dtype=np.uint8)
   img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

class ImgByteChange:
    def __init__(self):
        pass
    def ImageToByte(self,Img):
        tmpimg = Image.open(Img)
        with io.BytesIO() as output:
            tmpimg.save(output,format="JPEG")
            ImgToByte = output.getvalue()
            return ImgToByte

imgByteChange = ImgByteChange()
test = imgByteChange.ImageToByte("画像ファイル名.jpg") #
print(test)

with open ('ファイル名.dat','wb') as f: #open関数を使う際は絶対パスか相対パスでディレクトリを指定する事
  f.write(test)

# カレントディレクトリ（現在のディレクトリ）確認用コード
import os
print(os.getcwd())

# バイナリファイルを見やすく表示する(本番では要らない可能性高)
# https://qiita.com/sho11hei12-1998/items/372f6312908db27c4486
# https://issekinichou.wordpress.com/2019/02/27/python-binary/
# https://note.nkmk.me/python-bin-oct-hex-int-format/
f = open('ファイル名.dat', 'r+b')
all = f.read()
f.close()
hex_string = all.hex()
print(hex_string)
# 文字列をN文字ずつ分割
def splitStr(str, num):
    counter = 0
    w = ''
    strList = []
    for s in str:
        w += s
        counter += 1
        if counter == num:
            strList.append(w)
            counter = 0
            w = ''
    if w:
        strList.append(w)
    return strList

rows = splitStr(hex_string,32)
i = -1
for row in rows:
    byte = splitStr(row,2)
    i = i + 1
    j = i * 16
    print("0000", format(j, 'x'), byte)

# 復元可能な（←未検証）一部のバイナリデータを削除
# https://issekinichou.wordpress.com/2019/02/27/python-binary/

source1 = open('ファイル名.dat', 'r+b')
source1.seek(16 * 1 + 4)
data = source1.read()
#print (source1)
source1.close()

with open('ファイル名2.dat', 'wb') as f:
  f.seek(0)
  f.write(data)