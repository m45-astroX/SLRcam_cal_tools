#!/usr/bin/env python3

import numpy as np
import imageio.v2 as imageio
import argparse
import os

def adjust_brightness_contrast(image, brightness=0, contrast=1.0):
    """
    画像の明るさとコントラストを調整する
    brightness: -255 から +255 の範囲
    contrast: 0.1 以上の倍率
    """
    # 画像を float に変換して計算
    adjusted = image.astype(np.float32)
    
    # コントラストの適用
    adjusted = (adjusted - 127.5) * contrast + 127.5

    # 明るさの適用
    adjusted = adjusted + brightness

    # 0-255 にクリップし、uint8 に変換
    return np.clip(adjusted, 0, 255).astype(np.uint8)

def main():
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description="TIFF 画像の明るさとコントラストを調整するスクリプト")
    parser.add_argument("input_file", help="入力 TIFF ファイルのパス")
    parser.add_argument("output_file", help="出力 TIFF ファイルのパス")
    parser.add_argument("-b", "--brightness", type=int, default=0, help="明るさの調整値（-255 から +255, デフォルト: 0）")
    parser.add_argument("-c", "--contrast", type=float, default=1.0, help="コントラストの倍率（0.1 以上, デフォルト: 1.0）")

    args = parser.parse_args()

    # 入力 TIFF 画像の読み込み
    if not os.path.exists(args.input_file):
        print(f"エラー: ファイルが見つかりません: {args.input_file}")
        return

    image = imageio.imread(args.input_file)

    # 明るさとコントラストの調整
    adjusted_image = adjust_brightness_contrast(image, args.brightness, args.contrast)

    # 出力 TIFF 画像の保存
    imageio.imwrite(args.output_file, adjusted_image)
    print(f"明るさ {args.brightness}, コントラスト {args.contrast} を適用し、保存しました: {args.output_file}")

if __name__ == "__main__":
    main()
