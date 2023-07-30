#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Usage: python sgbpal_g.py palette_name pic.png

Colorize the Gen 1 Pokémon's sprites
with the SGB palettes of Pokémon Green.
Images will become indexed, with a palette sorted
{white, light color, dark color, black}.
"""

import png

import sys

def rgb8_to_rgb5(c):
	r, g, b = c
	return (r // 8, g // 8, b // 8)

def rgb5_to_rgb8(c):
	r, g, b = c
	return (r * 8 + r // 4, g * 8 + g // 4, b * 8 + b // 4)

def invert(c):
	r, g, b = c
	return (31 - r, 31 - g, 31 - b)

def luminance(c):
	r, g, b = c
	return 0.299 * r**2 + 0.587 * g**2 + 0.114 * b**2

def rgb5_pixels(row):
	yield from (rgb8_to_rgb5(row[x:x+3]) for x in range(0, len(row), 4))

def is_grayscale(palette):
	return (palette == ((31, 31, 31), (21, 21, 21), (10, 10, 10), (0, 0, 0)) or
		palette == ((31, 31, 31), (20, 20, 20), (10, 10, 10), (0, 0, 0)))

def colorize(filename, palette_name, palettes):
        with open(filename, "rb") as file:
                width, height, rows = png.Reader(file).asRGBA8()[:3]
                rows = list(rows)
        b_and_w = {(0, 0, 0), (31, 31, 31)}
        colors = {c for row in rows for c in rgb5_pixels(row)} - b_and_w
        if not colors:
        	colors = {(21, 21, 21), (10, 10, 10)}
        elif len(colors) == 1:
        	c = colors.pop()
        	colors = {c, invert(c)}
        elif len(colors) != 2:
        	return False
        palette = tuple(sorted(colors | b_and_w, key=luminance, reverse=True))
        assert len(palette) == 4
        rows = [list(map(palette.index, rgb5_pixels(row))) for row in rows]
        if is_grayscale(palette):
        	palette = tuple(map(rgb5_to_rgb8, palettes[palette_name]))
        	writer = png.Writer(width, height, palette=palette, bitdepth=8, compression=9)
        with open(filename, "wb") as file:
        	writer.write(file, rows)
        return True

def main():
        palettes = {"mewmon": ((30,31,29), (30,22,17), (16,14,19), (3,2,2)),
                    "bluemon": ((30,31,29), (18,20,27), (11,15,23), (3,2,2)),
                    "redmon": ((30,31,29), (31,20,10), (26,10,6), (3,2,2)),
                    "cyanmon": ((30,31,29), (21,25,29), (14,19,25), (3,2,2)),
                    "purplemon": ((30,31,29), (27,22,24), (21,15,23), (3,2,2)),
                    "brownmon": ((30,31,29), (28,20,15), (21,14,9), (3,2,2)),
                    "greenmon": ((30,31,29), (20,26,16), (9,20,11), (3,2,2)),
                    "pinkmon": ((30,31,29), (30,22,24), (28,15,21), (3,2,2)),
                    "yellowmon": ((30,31,29), (31,28,14), (26,20,0), (3,2,2)),
                    "graymon": ((30,31,29), (26,21,22), (15,15,18), (3,2,2))}
        usage = f"Usage: {sys.argv[0]} palette_name pic.png"
        if len(sys.argv) == 1:
                print(f"{usage}")
        elif len(sys.argv) > 1 and sys.argv[1].lower() == "-help":
                print(usage)
                print(f"\nPalette list and RGB888 values:")
                for k, v in palettes.items():
                        print("- " + k + ": " +
                              str(rgb5_to_rgb8(v[0])) + ", " +
                              str(rgb5_to_rgb8(v[1])) + ", " +
                              str(rgb5_to_rgb8(v[2])) + ", " +
                              str(rgb5_to_rgb8(v[3])))
        else:
                if sys.argv[1].lower() not in palettes:
                        print(f"Incorrect palette name!\nType -help to see all palettes", file=sys.stderr)
                        sys.exit(1)
                if len(sys.argv) == 2:
                        print(f"Please enter at least one valid PNG file!\n" + usage, file=sys.stderr)
                        sys.exit(1)
                else:
                        palette_name = sys.argv[1].lower()
                        for filename in sys.argv[2:]:
                                if not filename.lower().endswith('.png'):
                                        print(f"{filename} is not a .png file!", file=sys.stderr)
                                elif not colorize(filename, palette_name, palettes):
                                        print(f"{filename} has too many colors!", file=sys.stderr)
        		
if __name__ == '__main__':
	main()
