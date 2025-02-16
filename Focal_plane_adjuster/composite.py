#!/usr/bin/env python3

# composite.py

# 2025.02.15 v1.0 by Yuma Aoki


import rawpy
import numpy as np
import argparse
import cv2
import os
import imageio.v2 as imageio

def load_nef_images_from_directory(directory):
    
    nef_files = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith('.nef')])
    
    if not nef_files:
        print("*** Error")
        print("Infile does not exist!")
        print("abort.")
        return None

    images = []
    for nef_file in nef_files:
        with rawpy.imread(nef_file) as raw:
            rgb_image = raw.postprocess()
            images.append(rgb_image)
        print(f"Read: {nef_file}")

    return images if images else None

def composite_images(images, method):
    
    if not images:
        print("*** Error")
        print("Image does not exist!")
        print("abort.")
        return None

    # Read the size of images
    height, width, _ = images[0].shape
    stack = np.array(images, dtype=np.float32)

    if method == "mean" or method == "0" :
        result = np.mean(stack, axis=0)
    elif method == "max" or method == "1" :
        result = np.max(stack, axis=0)
    elif method == "min" or method == "2" :
        result = np.min(stack, axis=0)
    else:
        print("*** Error")
        print("Method must be 0, 1 or 2!")
        print("abort.")
        return None

    return np.clip(result, 0, 255).astype(np.uint8)

def main():
    
    # Method
    method = "mean"

    parser = argparse.ArgumentParser(description="This script composites nef files.")
    parser.add_argument("indir", help="The directory path where NEF files exist.")
    parser.add_argument("-o", "--output", default="composite_out.tif", help="The path of outfile(tiff format)")
    args = parser.parse_args()

    images = load_nef_images_from_directory(args.directory)

    if images:
        
        composite_image = composite_images(images, method)

        if composite_image is not None:
            
            imageio.imwrite(args.output, composite_image)
            print(f"Output: {args.output}")

if __name__ == "__main__":

    main()
