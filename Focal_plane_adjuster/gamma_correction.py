#!/usr/bin/env python3

import numpy as np
import imageio.v2 as imageio
import argparse
import os

def apply_gamma_correction(image, gamma):
    """
    ガンマ補正を適用する
    """
    # 画像を正規化 (0-255 → 0-1)
    normalized = image / 255.0
    # ガンマ補正: 出力 = 入力^(1/γ)
    corrected = np.power(normalized, 1.0 / gamma)
    # 0-255 に戻して uint8 に変換
    return np.clip(corrected * 255, 0, 255).astype(np.uint8)

def main():
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description="TIFF 画像にガンマ補正を適用するスクリプト")
    parser.add_argument("input_file", help="入力 TIFF ファイルのパス")
    parser.add_argument("output_file", help="出力 TIFF ファイルのパス")
    parser.add_argument("-g", "--gamma", type=float, default=2.2, help="ガンマ補正の値（デフォルト: 2.2）")

    args = parser.parse_args()

    # 入力 TIFF 画像の読み込み
    if not os.path.exists(args.input_file):
        print(f"エラー: ファイルが見つかりません: {args.input_file}")
        return

    image = imageio.imread(args.input_file)

    # ガンマ補正の適用
    corrected_image = apply_gamma_correction(image, args.gamma)

    # 出力 TIFF 画像の保存
    imageio.imwrite(args.output_file, corrected_image)
    print(f"ガンマ補正を適用し、保存しました: {args.output_file}")

if __name__ == "__main__":
    main()
