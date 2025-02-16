#!/usr/bin/env python3

# plot_profile.py

# 2025.02.16 v1.0 by Yuma Aoki

import rawpy
import numpy as np
import cv2
import argparse
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from skimage.draw import line
matplotlib.use('Agg')    # Not use matplot GUI


def get_line_values(image, x1, y1, x2, y2):

    rr, cc = line(y1, x1, y2, x2)
    rr = np.clip(rr, 0, image.shape[0] - 1)
    cc = np.clip(cc, 0, image.shape[1] - 1)

    r_values = image[rr, cc, 2].astype(np.uint16)
    g_values = image[rr, cc, 1].astype(np.uint16)
    b_values = image[rr, cc, 0].astype(np.uint16)

    return r_values, g_values, b_values, range(len(r_values))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("neffile", help="input NEF file")
    parser.add_argument("x1", type=int, help="Starting X Coordinate")
    parser.add_argument("y1", type=int, help="Starting Y Coordinate")
    parser.add_argument("x2", type=int, help="Ending X Coordinate")
    parser.add_argument("y2", type=int, help="Ending Y Coordinate")
    parser.add_argument("-r", "--red_csv", default="profile_red.csv", help="Output CSV Filename for the Red Channel")
    parser.add_argument("-g", "--green_csv", default="profile_green.csv", help="Output CSV Filename for the Green Channel")
    parser.add_argument("-b", "--blue_csv", default="profile_blue.csv", help="Output CSV Filename for the Blue Channel")
    parser.add_argument("-o", "--output", default="profile.png", help="Profile file name")

    args = parser.parse_args()

    with rawpy.imread(args.nef_file) as raw:
        rgb_image = raw.postprocess(output_bps=16)

    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

    r_values, g_values, b_values, indices = get_line_values(bgr_image, args.x1, args.y1, args.x2, args.y2)

    pd.DataFrame({"Pixel Index": indices, "Red": r_values}).to_csv(args.red_csv, index=False)
    pd.DataFrame({"Pixel Index": indices, "Green": g_values}).to_csv(args.green_csv, index=False)
    pd.DataFrame({"Pixel Index": indices, "Blue": b_values}).to_csv(args.blue_csv, index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(indices, r_values, 'r-', label='Red Channel')
    plt.plot(indices, g_values, 'g-', label='Green Channel')
    plt.plot(indices, b_values, 'b-', label='Blue Channel')

    plt.xlabel("Coordinate (pixels)")
    plt.ylabel("Pixel Intensity")
    plt.legend()
    plt.grid()

    plt.savefig(args.output)
    plt.close()

    
if __name__ == "__main__":

    main()
