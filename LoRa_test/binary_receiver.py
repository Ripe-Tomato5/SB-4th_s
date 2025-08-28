# 受信側は圧縮されたファイルを解凍する
# https://blog.amedama.jp/entry/2018/08/01/230413
with gzip.open('ファイル名2.dat.gz', 'rb') as fp:
  data2 = fp.read()
  print(data2)

# データ修復用バイナリデータを作成、先ほどのバイナリデータと合体
# # https://teratail.com/questions/329206
# https://af-e.net/python-file-creation/
# https://issekinichou.wordpress.com/2019/02/27/python-binary/
with open('ファイル名3.dat', 'wb') as f:
  binary_data = bytes.fromhex('ffd8ffe000000000000000000000000000000000')
  f.write(binary_data)
  f.close()

all = binary_data + data2
with open('ファイル名4.dat', 'wb') as f:
  f.seek(0)
  f.write(all)

# 編集したバイナリデータから画像を作成、保存
# https://machine-learning-skill-up.com/knowledge/python%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E7%94%BB%E5%83%8F%E3%82%92%E8%A1%A8%E7%A4%BA%E3%83%BB%E4%BF%9D%E5%AD%98%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95-%E5%88%9D%E5%BF%83%E8%80%85%E3%83%81%E3%83%A5
# https://elsammit-beginnerblg.hatenablog.com/entry/2020/12/08/232627
import os
import io
from PIL import Image
import numpy as np
from IPython.display import display

class ImgByteChange:
    def __init__(self):
        pass

    def ByteToImage(self, str):
        ByteToImg = Image.open(io.BytesIO(str))
        return ByteToImg

imgByteChange = ImgByteChange()
img = imgByteChange.ByteToImage(all)
display(img)
img.save("ファイル名5.jpg")