#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Usage: python g2rb.py pic.png

Convert the white SGB color of
Pokémon Green sprites to those
of Pokémon Red/Blue
"""

from PIL import Image

import sys

def g2rb(filename):
    img = Image.open(filename)
    img = img.convert("RGB")
    datas = img.getdata()
    new_image_data = []
    for item in datas:
        if item[0] == 247 and item[1] == 255 and item[2] == 239:
                new_image_data.append((255, 239, 255))
        else:
            new_image_data.append(item)
    img.putdata(new_image_data)
    img_index = img.convert("P", palette=Image.ADAPTIVE, colors=5)
    img_index.save(filename)
    return True

def main():
        if len(sys.argv) < 2:
                print(f"Usage: {sys.argv[0]} pic.png", file=sys.stderr)
                sys.exit(1)
        else:
                for filename in sys.argv[1:]:
                        if not filename.lower().endswith('.png'):
                                print(f"{filename} is not a .png file!", file=sys.stderr)
                        elif not g2rb(filename):
                                print(f"{filename}: error!", file=sys.stderr)
        		
if __name__ == '__main__':
	main()
