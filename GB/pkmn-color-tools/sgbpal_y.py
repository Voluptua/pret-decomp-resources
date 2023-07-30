#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Usage: python sgbpal_y.py mode palette_name pic.png

Colorize the Gen 1 Pokémon's sprites
with the SGB and GBC palettes of Pokémon Yellow.
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

def colorize(filename, palette_name, palettes_sgb, palettes_gbc, mode):
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
                if mode == "sgb":
                        palette = tuple(map(rgb5_to_rgb8, palettes_sgb[palette_name]))
                        writer = png.Writer(width, height, palette=palette, bitdepth=8, compression=9)
                elif mode == "gbc":
                        palette = tuple(map(rgb5_to_rgb8, palettes_gbc[palette_name]))
                        writer = png.Writer(width, height, palette=palette, bitdepth=8, compression=9)
        with open(filename, "wb") as file:
        	writer.write(file, rows)
        return True

def main():
        palettes_sgb = {"mewmon": ((31,31,30), (31,30,22), (27,16,16), (6,6,6)),
                        "bluemon": ((31,31,30), (21,22,31), (9,10,20), (6,6,6)),
                        "redmon": ((31,31,30), (31,24,11), (26,9,6), (6,6,6)),
                        "cyanmon": ((31,31,30), (26,28,31), (7,24,28), (6,6,6)),
                        "purplemon": ((31,31,30), (27,22,30), (22,15,23), (6,6,6)),
                        "brownmon": ((31,31,30), (26,23,18), (18,14,10), (6,6,6)),
                        "greenmon": ((31,31,30), (24,28,18), (13,21,15), (6,6,6)),
                        "pinkmon": ((31,31,30), (31,24,26), (31,18,21), (6,6,6)),
                        "yellowmon": ((31,31,30), (31,31,19), (28,23,9), (6,6,6)),
                        "graymon": ((31,31,30), (25,25,18), (16,16,14), (6,6,6))}
        palettes_gbc = {"mewmon": ((31,31,31), (31,31,0), (31,1,1), (3,3,3)),
                        "bluemon": ((31,31,31), (16,18,31), (0,1,25), (3,3,3)),
                        "redmon": ((31,31,31), (31,17,0), (31,0,0), (3,3,3)),
                        "cyanmon": ((31,31,31), (16,26,31), (0,17,31), (3,3,3)),
                        "purplemon": ((31,31,31), (25,15,31), (19,0,2), (3,3,3)),
                        "brownmon": ((31,31,31), (29,18,10), (17,9,5), (3,3,3)),
                        "greenmon": ((31,31,31), (17,31,11), (1,22,6), (3,3,3)),
                        "pinkmon": ((31,31,31), (31,15,18), (31,0,6), (3,3,3)),
                        "yellowmon": ((31,31,31), (31,31,0), (28,14,0), (3,3,3)),
                        "graymon": ((31,31,31), (20,23,10), (11,11,5), (3,3,3))}
        usage = f"Usage: {sys.argv[0]} mode palette_name pic.png"
        if len(sys.argv) == 1:
                print(f"{usage}")
        elif len(sys.argv) > 1 and sys.argv[1].lower() == "-help":
                print(usage)
                print(f"\nSGB palette list and RGB888 values:")
                for k, v in palettes_sgb.items():
                        print("- " + k + ": " +
                              str(rgb5_to_rgb8(v[0])) + ", " +
                              str(rgb5_to_rgb8(v[1])) + ", " +
                              str(rgb5_to_rgb8(v[2])) + ", " +
                              str(rgb5_to_rgb8(v[3])))
                print(f"\nGBC palette list and RGB888 values:")
                for k, v in palettes_gbc.items():
                        print("- " + k + ": " +
                              str(rgb5_to_rgb8(v[0])) + ", " +
                              str(rgb5_to_rgb8(v[1])) + ", " +
                              str(rgb5_to_rgb8(v[2])) + ", " +
                              str(rgb5_to_rgb8(v[3])))
        else:
                if sys.argv[1].lower() != "sgb" and sys.argv[1].lower() != "gbc":
                        print(f"Please enter a valid palette mode!\nYou can choose between sgb or gbc\n" + usage, file=sys.stderr)
                        sys.exit(1)
                else:
                        if len(sys.argv) == 2:
                                print(f"Please enter valid palette name and PNG file(s)!\n" + usage, file=sys.stderr)
                                sys.exit(1)
                        else:
                                if sys.argv[2].lower() not in palettes_sgb:
                                        print(f"Incorrect palette name!\nType -help to see all palettes", file=sys.stderr)
                                        sys.exit(1)
                                if len(sys.argv) == 3:
                                        print(f"Please enter at least one valid PNG file!\n" + usage, file=sys.stderr)
                                        sys.exit(1)
                                else:
                                        mode = sys.argv[1].lower()
                                        palette_name = sys.argv[2].lower()
                                        for filename in sys.argv[3:]:
                                                if not filename.lower().endswith('.png'):
                                                        print(f"{filename} is not a .png file!", file=sys.stderr)
                                                elif not colorize(filename, palette_name, palettes_sgb, palettes_gbc, mode):
                                                        print(f"{filename} has too many colors!", file=sys.stderr)

if __name__ == '__main__':
	main()
