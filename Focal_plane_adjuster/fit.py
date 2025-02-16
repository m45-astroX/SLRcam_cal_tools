#!/usr/bin/env python3

# fit.py

# 2025.02.16 v1.0 by Yuma Aoki


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

    parser = argparse.ArgumentParser(description="2Lorentzians + Gaussian Fitting Script")

    parser.add_argument("csv_file", help="Path to the csv File for Fitting")
    parser.add_argument("-o", "--output", default="fit_result.png", help="出力画像ファイル名 (default: fit_result.png)")
    parser.add_argument("-p", "--param", default="fit_parameters.csv", help="出力パラメータcsv (default: fit_parameters.csv)")

    parser.add_argument("--lc1", type=float, required=True, metavar="LC1", help="Center of Lorentzian 1")
    parser.add_argument("--ln1", type=float, required=True, metavar="LN1", help="Height of Lorentzian 1")
    parser.add_argument("--lw1", type=float, default=2.0,   metavar="LW1", help="Width of Lorentzian 1 (default=2.0)")

    parser.add_argument("--lc2", type=float, required=True, metavar="LC2", help="Center of Lorentzian 2")
    parser.add_argument("--ln2", type=float, required=True, metavar="LN2", help="Height of Lorentzian 2")
    parser.add_argument("--lw2", type=float, default=2.0,   metavar="LW2", help="Width of Lorentzian 2 (default=2.0)")

    parser.add_argument("--lc3", type=float, required=True, metavar="LC3", help="Center of Lorentzian 3")
    parser.add_argument("--ln3", type=float, required=True, metavar="LN3", help="Height of Lorentzian 3")
    parser.add_argument("--lw3", type=float, default=2.0,   metavar="LW3", help="Width of Lorentzian 3 (default=2.0)")

    parser.add_argument("--gc", type=float, required=True, metavar="GC", help="Center of Gaussian")
    parser.add_argument("--gn", type=float, required=True, metavar="GN", help="Height of Gaussian")
    parser.add_argument("--gw", type=float, default=100.0, metavar="GW", help="Width of Gaussian (default=100.0)")

    args = parser.parse_args()

    if not os.path.exists(args.csv_file):
        print("*** Error ***")
        print("csvfile does not exist!")
        print("abort.")
        return

    df = pd.read_csv(args.csv_file)
    x_data = df.iloc[:, 0].values
    y_data = df.iloc[:, 1].values

    initial_params = [
        args.ln1, args.lc1, args.lw1,
        args.ln2, args.lc2, args.lw2,
        args.ln3, args.lc3, args.lw3,
        args.gn, args.gc, args.gw
    ]

    popt, pcov = curve_fit(combined_function, x_data, y_data, p0=initial_params)

    ln1_fit, lc1_fit, lw1_fit, ln2_fit, lc2_fit, lw2_fit, ln3_fit, lc3_fit, lw3_fit, gn_fit, gc_fit, gw_fit = popt

    print(f"Lorentzian1 : LC = {lc1_fit:.3f}, LN = {ln1_fit:.3f}, LW = {lw1_fit:.3f}")
    print(f"Lorentzian2 : LC = {lc2_fit:.3f}, LN = {ln2_fit:.3f}, LW = {lw2_fit:.3f}")
    print(f"Lorentzian3 : LC = {lc3_fit:.3f}, LN = {ln3_fit:.3f}, LW = {lw3_fit:.3f}")
    print(f"Gaussian    : GC = {gc_fit:.3f}, GN = {gn_fit:.3f}, GW = {gw_fit:.3f}")

    x_fit = np.linspace(min(x_data), max(x_data), 500)
    y_fit = combined_function(x_fit, *popt)

    plt.figure(figsize=(8, 6))
    #plt.scatter(x_data, y_data, label="Original Data", color="black", s=10)
    #plt.plot(x_fit, y_fit, label="Fitted Curve", color="red", linewidth=2)
    #plt.title("Lorentzian + Lorentzian + Lorentzian + Gaussian Fit")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid()

    plt.savefig(args.output)
    plt.close()

    fit_results = pd.DataFrame({
        "Function": ["Lorentzian1", "Lorentzian2", "Lorentzian3", "Gaussian"],
        "Center": [lc1_fit, lc2_fit, lc3_fit, gc_fit],
        "Height": [ln1_fit, ln2_fit, ln3_fit, gn_fit],
        "Width": [lw1_fit, lw2_fit, lw3_fit, gw_fit]
    })
    fit_results.to_csv(args.param, index=False)


if __name__ == "__main__":
    
    main()
