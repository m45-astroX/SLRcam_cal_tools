import rawpy
import numpy as np
import cv2
import matplotlib
import pandas as pd
matplotlib.use('Agg')  # GUIを使わないバックエンド
import matplotlib.pyplot as plt
from skimage.draw import line

def get_line_values(image, x1, y1, x2, y2):
    """
    2つの座標 (x1, y1) から (x2, y2) までの直線上のピクセル値を取得する。
    """
    # 直線上のピクセルの座標を取得
    rr, cc = line(y1, x1, y2, x2)  # skimage.draw.line は (row, col) = (y, x)
    
    # 画像サイズを超えないように制限
    rr = np.clip(rr, 0, image.shape[0] - 1)
    cc = np.clip(cc, 0, image.shape[1] - 1)

    # 各チャンネルの値を取得
    r_values = image[rr, cc, 2]  # OpenCVはBGRなので、Rは2番目
    g_values = image[rr, cc, 1]  # Gは1番目
    b_values = image[rr, cc, 0]  # Bは0番目

    return r_values, g_values, b_values, range(len(r_values))

# NEF 画像ファイル
nef_file = "sample.nef"

# 画像の読み込み
with rawpy.imread(nef_file) as raw:
    rgb_image = raw.postprocess()

# OpenCV 用に BGR に変換
bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

# 画像のサイズを取得
height, width, _ = bgr_image.shape

# 2つの座標をユーザーに入力させる
print("画像サイズ:", width, "x", height)
x1, y1 = map(int, input("始点の座標 (x1, y1) を入力: ").split())
x2, y2 = map(int, input("終点の座標 (x2, y2) を入力: ").split())

# 直線上のピクセル値を取得
r_values, g_values, b_values, indices = get_line_values(bgr_image, x1, y1, x2, y2)

# **RGB 各チャンネルの CSV ファイルとして保存**
output_red_csv = "pixel_intensity_red.csv"
output_green_csv = "pixel_intensity_green.csv"
output_blue_csv = "pixel_intensity_blue.csv"

pd.DataFrame({"Pixel Index": indices, "Red": r_values}).to_csv(output_red_csv, index=False)
pd.DataFrame({"Pixel Index": indices, "Green": g_values}).to_csv(output_green_csv, index=False)
pd.DataFrame({"Pixel Index": indices, "Blue": b_values}).to_csv(output_blue_csv, index=False)

# **グラフの描画（画像として保存）**
plt.figure(figsize=(8, 5))
plt.plot(indices, r_values, 'r-', label='Red Channel')
plt.plot(indices, g_values, 'g-', label='Green Channel')
plt.plot(indices, b_values, 'b-', label='Blue Channel')

plt.xlabel("Pixel Index Along Line")
plt.ylabel("Pixel Intensity (0-255)")
plt.title("Pixel Intensity Along Selected Line")
plt.legend()
plt.grid()

# **グラフを保存**
output_graph = "pixel_intensity_plot.png"
plt.savefig(output_graph)
plt.close()

# **完了メッセージ**
print(f"グラフを {output_graph} に保存しました。")
print(f"Red チャンネルのデータを {output_red_csv} に保存しました。")
print(f"Green チャンネルのデータを {output_green_csv} に保存しました。")
print(f"Blue チャンネルのデータを {output_blue_csv} に保存しました。")
