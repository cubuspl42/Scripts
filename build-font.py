from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph

# Load the original font
font = TTFont("input.ttf")

# Define an empty glyph
empty_glyph = Glyph()
empty_glyph.width = 1

# Replace the glyph for the NBSP character
font["glyf"]["uni00A0"] = empty_glyph

# Remove all other characters
for char in list(font["glyf"].glyphs.keys()):
    if char != "uni00A0":
        del font["glyf"][char]

Save the modified font
font.save("output.ttf")