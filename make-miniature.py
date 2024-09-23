#!/usr/bin/env python3

import argparse
from PIL import Image

def resize_and_crop(img_path, modified_img_path, size):
    try:
        img = Image.open(img_path)
        img.thumbnail(size, Image.LANCZOS)
        width, height = img.size

        if width > height:
            left = (width - height)/2
            top = 0
            right = (width + height)/2
            bottom = height
        else:
            top = (height - width)/2
            bottom = (height + width)/2
            left = 0
            right = width

        img = img.crop((left, top, right, bottom))
        img = img.resize(size, Image.LANCZOS)
        img.save(modified_img_path)
        print(f"Image saved as {modified_img_path}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Resize and crop an image.')
    parser.add_argument('input_image', type=str, help='Path to the input image.')
    parser.add_argument('output_image', type=str, help='Path to save the output image.')
    parser.add_argument('--size', type=int, default=256, help='Square side width.')
    args = parser.parse_args()

    size = (args.size, args.size)
    resize_and_crop(args.input_image, args.output_image, size)

if __name__ == "__main__":
    main()
