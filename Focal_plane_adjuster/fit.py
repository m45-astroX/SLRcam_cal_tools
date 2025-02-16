#!/usr/bin/env python3

# fit.py
# 2025.02.16 v1.2 by Yuma Aoki

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from scipy.optimize import curve_fit
import os

def lorentzian(x, A, x0, gamma):
    return (A * gamma**2) / ((x - x0)**2 + gamma**2)

def gaussian(x, A, x0, sigma):
    return A * np.exp(-((x - x0) ** 2) / (2 * sigma ** 2))

def combined_function(x, A1, x01, gamma1, A2, x02, gamma2, A3, x03, gamma3, A4, x04, sigma4):
    return (lorentzian(x, A1, x01, gamma1) +
            lorentzian(x, A2, x02, gamma2) +
            lorentzian(x, A3, x03, gamma3) +
            gaussian(x, A4, x04, sigma4))

def main():
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description="Lorentzian + Gaussian Fitting Script")

    # 必須引数
    parser.add_argument("csv_file", help="フィッティングするCSVファイルのパス")

    # 出力ファイル
    parser.add_argument("-o", "--output", default="fit_result.png", help="出力画像ファイル名（デフォルト: fit_result.png）")
    parser.add_argument("-p", "--param", default="fit_parameters.csv", help="出力パラメータCSV（デフォルト: fit_parameters.csv）")

    # 各ピークの初期値
    parser.add_argument("--lc1", type=float, required=True, metavar="LC1", help="Lorentzian 1 の中心値")
    parser.add_argument("--ln1", type=float, required=True, metavar="LN1", help="Lorentzian 1 の高さ")
    parser.add_argument("--lw1", type=float, default=2.0, metavar="LW1", help="Lorentzian 1 の幅（デフォルト: 2.0）")

    parser.add_argument("--lc2", type=float, required=True, metavar="LC2", help="Lorentzian 2 の中心値")
    parser.add_argument("--ln2", type=float, required=True, metavar="LN2", help="Lorentzian 2 の高さ")
    parser.add_argument("--lw2", type=float, default=2.0, metavar="LW2", help="Lorentzian 2 の幅（デフォルト: 2.0）")

    parser.add_argument("--lc3", type=float, required=True, metavar="LC3", help="Lorentzian 3 の中心値")
    parser.add_argument("--ln3", type=float, required=True, metavar="LN3", help="Lorentzian 3 の高さ")
    parser.add_argument("--lw3", type=float, default=2.0, metavar="LW3", help="Lorentzian 3 の幅（デフォルト: 2.0）")

    parser.add_argument("--gc", type=float, required=True, metavar="GC", help="Gaussian の中心値")
    parser.add_argument("--gn", type=float, required=True, metavar="GN", help="Gaussian の高さ")
    parser.add_argument("--gw", type=float, default=2.0, metavar="GW", help="Gaussian の幅（デフォルト: 2.0）")

    args = parser.parse_args()

    # CSVファイルの存在確認
    if not os.path.exists(args.csv_file):
        print("*** Error")
        print("CSVファイルが存在しません！")
        print("abort.")
        return

    # CSVデータの読み込み
    df = pd.read_csv(args.csv_file)
    x_data = df.iloc[:, 0].values
    y_data = df.iloc[:, 1].values

    # 初期パラメータの設定
    initial_params = [
        args.ln1, args.lc1, args.lw1,
        args.ln2, args.lc2, args.lw2,
        args.ln3, args.lc3, args.lw3,
        args.gn, args.gc, args.gw
    ]

    # フィッティングの実行
    popt, pcov = curve_fit(combined_function, x_data, y_data, p0=initial_params)

    # フィッティング結果を取得
    ln1_fit, lc1_fit, lw1_fit, ln2_fit, lc2_fit, lw2_fit, ln3_fit, lc3_fit, lw3_fit, gn_fit, gc_fit, gw_fit = popt

    print("\n=== フィッティング結果 ===")
    print(f"Lorentzian 1: 中心 = {lc1_fit:.3f}, 高さ = {ln1_fit:.3f}, 幅 = {lw1_fit:.3f}")
    print(f"Lorentzian 2: 中心 = {lc2_fit:.3f}, 高さ = {ln2_fit:.3f}, 幅 = {lw2_fit:.3f}")
    print(f"Lorentzian 3: 中心 = {lc3_fit:.3f}, 高さ = {ln3_fit:.3f}, 幅 = {lw3_fit:.3f}")
    print(f"Gaussian: 中心 = {gc_fit:.3f}, 高さ = {gn_fit:.3f}, 幅 = {gw_fit:.3f}")

    # フィッティング結果をプロット
    x_fit = np.linspace(min(x_data), max(x_data), 500)
    y_fit = combined_function(x_fit, *popt)

    plt.figure(figsize=(8, 6))
    plt.scatter(x_data, y_data, label="Original Data", color="black", s=10)
    plt.plot(x_fit, y_fit, label="Fitted Curve", color="red", linewidth=2)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Lorentzian + Lorentzian + Lorentzian + Gaussian Fit")
    plt.legend()
    plt.grid()

    # グラフ保存
    plt.savefig(args.output)
    plt.close()

    # フィッティングデータをCSVに保存
    fit_results = pd.DataFrame({
        "Function": ["Lorentzian 1", "Lorentzian 2", "Lorentzian 3", "Gaussian"],
        "Center": [lc1_fit, lc2_fit, lc3_fit, gc_fit],
        "Height": [ln1_fit, ln2_fit, ln3_fit, gn_fit],
        "Width": [lw1_fit, lw2_fit, lw3_fit, gw_fit]
    })
    fit_results.to_csv(args.param, index=False)

    print(f"\nフィッティング結果のプロットを {args.output} に保存しました。")
    print(f"フィッティングパラメータを {args.param} に保存しました。")

if __name__ == "__main__":
    main()
