#!/usr/bin/env python3

import numpy as np
import imageio.v2 as imageio
import argparse
import os

def apply_gamma_correction(image, gamma):
    """
    16bit TIFF画像にガンマ補正を適用
    """
    dtype = image.dtype
    max_val = 65535 if dtype == np.uint16 else 255

    normalized = image.astype(np.float32) / max_val
    corrected = np.power(normalized, 1.0 / gamma)
    return np.clip(corrected * max_val, 0, max_val).astype(dtype)

def main():
    parser = argparse.ArgumentParser(description="TIFF 画像にガンマ補正を適用するスクリプト（16bit対応）")
    parser.add_argument("input_file", help="入力 TIFF ファイルのパス")
    parser.add_argument("output_file", help="出力 TIFF ファイルのパス")
    parser.add_argument("-g", "--gamma", type=float, default=2.2, help="ガンマ補正の値（デフォルト: 2.2）")

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"エラー: ファイルが見つかりません: {args.input_file}")
        return

    image = imageio.imread(args.input_file)

    corrected_image = apply_gamma_correction(image, args.gamma)

    imageio.imwrite(args.output_file, corrected_image)
    print(f"ガンマ補正を適用し、保存しました: {args.output_file}")

if __name__ == "__main__":
    main()
