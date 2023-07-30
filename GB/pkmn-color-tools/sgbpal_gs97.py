#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Usage: python sgbpal_gs97.py (shiny) palette_name pic.png

Colorize the Gen 1/2 Pokémon's sprites
with the SGB palettes of the prototypes of Pokémon
Gold/Silver from the 1997 Nintendo Space World.
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

def colorize(filename, palette_name, palettes, palettes_shiny, mode):
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
                if mode == "normal":
                        palette = tuple(map(rgb5_to_rgb8, palettes[palette_name]))
                        writer = png.Writer(width, height, palette=palette, bitdepth=8, compression=9)
                elif mode == "shiny":
                        palette = tuple(map(rgb5_to_rgb8, palettes_shiny[palette_name]))
                        writer = png.Writer(width, height, palette=palette, bitdepth=8, compression=9)
        with open(filename, "wb") as file:
        	writer.write(file, rows)
        return True

def main():
        palettes = {"mewmon": ((28,28,28), (30,22,17), (16,14,19), (4,4,4)),
                    "bluemon": ((28,28,28), (18,20,27), (11,15,23), (4,4,4)),
                    "redmon": ((28,28,28), (31,20,10), (26,10,6), (4,4,4)),
                    "cyanmon": ((28,28,28), (21,25,29), (14,19,25), (4,4,4)),
                    "purplemon": ((28,28,28), (27,22,24), (21,15,23), (4,4,4)),
                    "brownmon": ((28,28,28), (28,20,15), (21,14,9), (4,4,4)),
                    "greenmon": ((28,28,28), (20,26,16), (9,20,11), (4,4,4)),
                    "pinkmon": ((28,28,28), (30,22,24), (28,15,21), (4,4,4)),
                    "yellowmon": ((28,28,28), (31,28,14), (26,20,0), (4,4,4)),
                    "graymon": ((28,28,28), (26,21,22), (15,15,18), (4,4,4))}
        palettes_shiny = {"mewmon": ((28,28,28), (23,19,13), (14,12,17), (4,4,4)),
                          "bluemon": ((28,28,28), (16,18,21), (10,12,18), (4,4,4)),
                          "redmon": ((28,28,28), (22,15,16), (17,2,5), (4,4,4)),
                          "cyanmon": ((28,28,28), (15,20,20), (5,16,16), (4,4,4)),
                          "purplemon": ((28,28,28), (23,15,19), (14,4,12), (4,4,4)),
                          "brownmon": ((28,28,28), (20,17,18), (18,13,11), (4,4,4)),
                          "greenmon": ((28,28,28), (23,21,16), (12,12,10), (4,4,4)),
                          "pinkmon": ((28,28,28), (21,25,29), (30,22,24), (4,4,4)),
                          "yellowmon": ((28,28,28), (26,23,16), (29,14,9), (4,4,4)),
                          "graymon": ((28,28,28), (18,18,18), (10,10,10), (4,4,4))}
        usage = f"Usage: {sys.argv[0]} (shiny) palette_name pic.png"
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
                print(f"\nShiny palette list and RGB888 values:")
                for k, v in palettes_shiny.items():
                        print("- " + k + ": " +
                              str(rgb5_to_rgb8(v[0])) + ", " +
                              str(rgb5_to_rgb8(v[1])) + ", " +
                              str(rgb5_to_rgb8(v[2])) + ", " +
                              str(rgb5_to_rgb8(v[3])))
        else:
                if sys.argv[1].lower() == "shiny":
                        if len(sys.argv) == 2:
                                print(f"Please enter valid palette name and PNG file(s)!\n" + usage, file=sys.stderr)
                                sys.exit(1)
                        else:
                                if sys.argv[2].lower() not in palettes:
                                        print(f"Incorrect palette name!\nType -help to see all palettes", file=sys.stderr)
                                        sys.exit(1)
                                if len(sys.argv) == 3:
                                        print(f"Please enter at least one valid PNG file!\n" + usage, file=sys.stderr)
                                        sys.exit(1)
                                else:
                                        mode = "shiny"
                                        palette_name = sys.argv[2].lower()
                                        for filename in sys.argv[3:]:
                                                if not filename.lower().endswith('.png'):
                                                        print(f"{filename} is not a .png file!", file=sys.stderr)
                                                elif not colorize(filename, palette_name, palettes, palettes_shiny, mode):
                                                        print(f"{filename} has too many colors!", file=sys.stderr)
                else:
                        if sys.argv[1].lower() not in palettes:
                                print(f"Incorrect palette name!\nType -help to see all palettes", file=sys.stderr)
                                sys.exit(1)
                        if len(sys.argv) == 2:
                                print(f"Please enter at least one valid PNG file!\n" + usage, file=sys.stderr)
                                sys.exit(1)
                        else:
                                mode = "shiny"
                                palette_name = sys.argv[1].lower()
                                for filename in sys.argv[2:]:
                                        if not filename.lower().endswith('.png'):
                                                print(f"{filename} is not a .png file!", file=sys.stderr)
                                        elif not colorize(filename, palette_name, palettes, palettes_shiny, mode):
                                                print(f"{filename} has too many colors!", file=sys.stderr)
        		
if __name__ == '__main__':
	main()
