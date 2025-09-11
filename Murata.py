import numpy as np
import matplotlib.pyplot as plt
import cv2

class murata():
    def __init__(self):
        pass

    def posterization(image, levels):
        # LUTを作成    
        x = np.arange(0, 256)  # [0, 1, 2, ..., 255]
        divider = np.linspace(0, 255, levels + 1)[1]
        quantiz = np.linspace(0, 255, levels, dtype=np.uint8)
        color_levels = np.clip((x / divider).astype(np.uint8), 0, levels - 1)
        y = quantiz[color_levels]

        # 変換
        posterized = cv2.LUT(image, y)
        return posterized, y

    def posterize_main(photo_name):
        # 画像の読み込み
        image = cv2.imread(photo_name)
        # 色数を減らすため、ぼかしを適用
        blurred = cv2.bilateralFilter(cv2.blur(image, (3, 3)), 9, 75, 75)
        # 階調数を設定（256がなぜか一番削減できる）
        levels = 256
        # ポスタライズ
        posterized, table = posterization(blurred, levels)
        # BGRのチャンネル並びをRGBの並びに変更(matplotlibで結果を表示するため)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        posterized = cv2.cvtColor(posterized, cv2.COLOR_BGR2RGB) 
        # 結果の可視化
        plt.imshow(posterized)                          # 修復後の画像を表示
        plt.axis("off")                                 # 軸目盛、軸ラベルを消す
        plt.savefig("Artistic_Murata.jpg")  # 画像を保存
        print("撮影画像のポスタライズ化に成功しました")

    def size_reduce(photo_name):
        im = cv2.imread(photo_name)
        cv2.imwrite(photo_name, im, [int(cv2.IMWRITE_JPEG_QUALITY), 20]) # 画質は荒くなるが10にするとデータをさらに削減できる
        print("撮影画像のデータサイズ圧縮に成功しました")

def main():
    mr = murata()