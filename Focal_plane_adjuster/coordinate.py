#!/usr/bin/env python3

# coordinate.py
# - tifファイルにピクセル座標を描画するスクリプト

# 2025.02.16 v1.0 by Yuma Aoki


import numpy as np
import cv2
import argparse
import os

def draw_grid(image, grid_size):
    
    height, width = image.shape[:2]
    dtype = image.dtype
    is_grayscale = len(image.shape) == 2

    color = 65535 if dtype == np.uint16 else 255
    thickness = 2 if dtype == np.uint16 else 1

    for x in range(0, width, grid_size):
        cv2.line(image, (x, 0), (x, height), (0, color, 0) if not is_grayscale else color, thickness)
    for y in range(0, height, grid_size):
        cv2.line(image, (0, y), (width, y), (0, color, 0) if not is_grayscale else color, thickness)

    return image


def main():

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("infile(.tif)", help="")
    parser.add_argument("-g", "--grid", type=int, default=100, help="Grid spacing (default: 100 pixels)")
    parser.add_argument("-o", "--output", default="grid.png", help="Output file name (default: grid.png)")

    args = parser.parse_args()

    if not os.path.exists(args.tiff_file):
        print("*** Error ***")
        print("infile does not exist!")
        print("abort.")
        return

    image = cv2.imread(args.tiff_file, cv2.IMREAD_UNCHANGED)

    if image is None:
        print("*** Error ***")
        print("Failed to load infile!")
        print("abort.")
        return

    image_with_grid = draw_grid(image, args.grid)

    cv2.imwrite(args.output, image_with_grid)


if __name__ == "__main__":

    main()
