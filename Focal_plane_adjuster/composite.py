#!/usr/bin/env python3

# composite.py
# - NEFファイルをコンポジットするスクリプト

# 2025.02.16 v1.0 by Yuma Aoki


import numpy as np
import argparse
import cv2
import os
import rawpy
import imageio.v2 as imageio


def load_nef_images_from_directory(directory):
    
    nef_files = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith('.nef')])

    if not nef_files:
        print("*** Error ***")
        print("No NEF files found.")
        print("abort.")
        return None

    images = []
    for nef_file in nef_files:
        try:
            with rawpy.imread(nef_file) as raw:
                image = raw.postprocess(output_bps=16)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                images.append(image)
                print(f"Load: {nef_file}")
        except Exception as e:
            print("*** Error ***")
            print(f"Failed to load: {nef_file}")
            print("skip.")
            continue

    return images if images else None


def composite_images(images, method):
    
    if not images:
        print("*** Error ***")
        print("No valid images to process.")
        print("abort.")
        return None

    stack = np.array(images, dtype=np.float32)

    if method == "mean":
        result = np.mean(stack, axis=0)
    elif method == "max":
        result = np.max(stack, axis=0)
    elif method == "min":
        result = np.min(stack, axis=0)
    else:
        print("*** Error ***")
        print("Invalid composite method.")
        print("abort.")
        return None

    return np.clip(result, 0, 65535).astype(np.uint16)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("indir", help="")
    parser.add_argument("-o", "--outfile", default="composite.tif", help="")
    parser.add_argument("-m", "--method", choices=["mean", "max", "min"], default="mean", help="")

    args = parser.parse_args()

    images = load_nef_images_from_directory(args.indir)

    if images:
        composite_image = composite_images(images, args.method)

        if composite_image is not None:
            imageio.imwrite(args.output, composite_image)
            print(f"Save: {args.output}")


if __name__ == "__main__":

    main()
