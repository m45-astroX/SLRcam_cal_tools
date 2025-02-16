#!/usr/bin/env python3

import numpy as np
import imageio.v2 as imageio
import argparse
import os

def adjust_brightness_contrast(image, brightness=0, contrast=1.0):
    """
    16bit TIFF画像の明るさとコントラストを調整する
    """
    dtype = image.dtype
    max_val = 65535 if dtype == np.uint16 else 255

    adjusted = image.astype(np.float32)

    # コントラスト調整
    adjusted = (adjusted - max_val / 2) * contrast + max_val / 2

    # 明るさ調整
    adjusted = adjusted + brightness * (max_val / 255)

    return np.clip(adjusted, 0, max_val).astype(dtype)

def main():
    parser = argparse.ArgumentParser(description="TIFF 画像の明るさとコントラストを調整するスクリプト（16bit対応）")
    parser.add_argument("input_file", help="入力 TIFF ファイルのパス")
    parser.add_argument("output_file", help="出力 TIFF ファイルのパス")
    parser.add_argument("-b", "--brightness", type=int, default=0, help="明るさ調整（-255 から +255, デフォルト: 0）")
    parser.add_argument("-c", "--contrast", type=float, default=1.0, help="コントラスト調整（0.1 以上, デフォルト: 1.0）")

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"エラー: ファイルが見つかりません: {args.input_file}")
        return

    image = imageio.imread(args.input_file)

    adjusted_image = adjust_brightness_contrast(image, args.brightness, args.contrast)

    imageio.imwrite(args.output_file, adjusted_image)
    print(f"明るさ {args.brightness}, コントラスト {args.contrast} を適用し、保存しました: {args.output_file}")

if __name__ == "__main__":
    main()
