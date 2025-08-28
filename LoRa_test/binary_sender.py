# https://invisiblepotato.com/google-colaboratory01/#vnc-viewer%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB-pc%E6%93%8D%E4%BD%9C

from PIL import Image
from IPython.display import display

# 画像を読み込む
img = Image.open("画像ファイル名")

# 画像を表示
display(img)

# jpegファイルをバイナリデータに変換、バイナリファイルを出力するプログラム
# https://elsammit-beginnerblg.hatenablog.com/entry/2020/12/08/232627

import os
import io
from PIL import Image
import numpy as np

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
test = imgByteChange.ImageToByte("画像ファイル名.jpg")
print(test)

with open ('ファイル名.dat','wb') as f:
  f.write(test)

# バイナリファイルを見やすく表示する
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

# 復元可能な（と思われる）一部のバイナリデータを削除
# https://issekinichou.wordpress.com/2019/02/27/python-binary/

source1 = open('ファイル名.dat', 'r+b')
source1.seek(16 * 1 + 4)
data = source1.read()
#print (source1)
source1.close()

with open('ファイル名2.dat', 'wb') as f:
  f.seek(0)
  f.write(data)

input()

# gzipを使いバイナリデータを圧縮して送信
# https://blog.amedama.jp/entry/2018/08/01/230413
source2 = open('ファイル名2.dat', 'r+b')
data2 = source2.read()
source2.close()
import gzip
with gzip.open('ファイル名2.dat.gz', 'wb') as fp:
  fp.write(data2)