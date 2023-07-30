# pkmn-color-tools
Tools to manipulate the colors of the sprites of the first *Pokémon* games.

All Python scripts have been adapted from this one: https://github.com/pret/pokered/blob/master/tools/palfix.py

## g2rb.py
Usage: `python g2rb.py pic.png`

Convert the white SGB color of *Pokémon Green* sprites to those of *Pokémon Red*/*Blue*. Images will become indexed.

## rb2g.py
Usage: `python rb2g.py pic.png`

Convert the white SGB color of *Pokémon Red*/*Blue* sprites to those of *Pokémon Green*. Images will become indexed.

## sgbpal_g.py
Usage: `python sgbpal_g.py palette_name pic.png`

Colorize the Gen 1 Pokémon's sprites with the SGB palettes of *Pokémon Green*. Images will become indexed, with a palette sorted {white, light color, dark color, black}.

## sgbpal_gs97.py
Usage: `python sgbpal_gs97.py (shiny) palette_name pic.png`

Colorize the Gen 1/2 Pokémon's sprites with the SGB palettes of the prototypes of *Pokémon Gold/Silver* from the 1997 Nintendo Space World. Images will become indexed, with a palette sorted {white, light color, dark color, black}.

## sgbpal_rb.py
Usage: `python sgbpal_rb.py palette_name pic.png`

Colorize the Gen 1 Pokémon's sprites with the SGB palettes of *Pokémon Red*/*Blue*. Images will become indexed, with a palette sorted {white, light color, dark color, black}.

## sgbpal_y.py
Usage: `python sgbpal_y.py mode palette_name pic.png`

Colorize the Gen 1 Pokémon's sprites with the SGB and GBC palettes of *Pokémon Yellow*. Images will become indexed, with a palette sorted {white, light color, dark color, black}.
