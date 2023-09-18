# You are likely to use these libraries
from PIL import Image, ImageDraw
import numpy as np

# Start a new blank canvas
image = Image.new("RGB", (2500, 2500), (255, 255, 255))

# Use the draw object to draw objects
draw = ImageDraw.Draw(image)

# Define a disorted re-centered ellipse
def distorted_ellipse(draw_obj, topleft_xy, bottomright_xy, center_xy, fill_rgb, quadrants=(True, True, True, True), stroke_width=(0, 0, 0, 0)):
    # Given a corner and a center, determine the opposiste corner
    # If you draw this on paper, the other corner is on the opposite side of the center
    # that the original corner is
    def opposite_corner(corner, center):
        return (2*center[0] - corner[0], 2*center[1] - corner[1])
    # Top left
    if quadrants[0]:
        draw_obj.pieslice(xy=[topleft_xy,
                            opposite_corner(topleft_xy, center_xy)],
                            start=180,
                            end=270,
                            fill=fill_rgb)
        if stroke_width[0]:
            draw_obj.arc(xy=[topleft_xy,
                            opposite_corner(topleft_xy, center_xy)],
                            start=180,
                            end=270,
                            fill="black",
                            width=stroke_width[0])
    # Top right
    if quadrants[1]:
        topright_xy = (bottomright_xy[0], topleft_xy[1])
        topright_xy_opp = opposite_corner(topright_xy, center_xy)
        draw_obj.pieslice(xy=[(topright_xy_opp[0], topright_xy[1]),
                            (topright_xy[0], topright_xy_opp[1])],
                            start=270,
                            end=0,
                            fill=fill_rgb)
        if stroke_width[1]:
            draw_obj.arc(xy=[(topright_xy_opp[0], topright_xy[1]),
                            (topright_xy[0], topright_xy_opp[1])],
                            start=270,
                            end=0,
                            fill="black",
                            width=stroke_width[1])
    # Bottom right
    if quadrants[2]:
        bottomright_xy_opp = opposite_corner(bottomright_xy, center_xy)
        draw_obj.pieslice(xy=[(bottomright_xy_opp[0], bottomright_xy_opp[1]),
                            (bottomright_xy[0], bottomright_xy[1])],
                            start=0,
                            end=90,
                            fill=fill_rgb)
        if stroke_width[2]:
            draw_obj.arc(xy=[(bottomright_xy_opp[0], bottomright_xy_opp[1]),
                            (bottomright_xy[0], bottomright_xy[1])],
                            start=0,
                            end=90,
                            fill="black",
                            width=stroke_width[2])
    # Bottom left
    if quadrants[3]:
        bottomleft_xy = (topleft_xy[0], bottomright_xy[1])
        bottomleft_xy_opp = opposite_corner(bottomleft_xy, center_xy)
        draw_obj.pieslice(xy=[(bottomleft_xy[0], bottomleft_xy_opp[1]),
                            (bottomleft_xy_opp[0], bottomleft_xy[1])],
                            start=90,
                            end=180,
                            fill=fill_rgb)
        if stroke_width[3]:
            draw_obj.arc(xy=[(bottomleft_xy[0], bottomleft_xy_opp[1]),
                            (bottomleft_xy_opp[0], bottomleft_xy[1])],
                            start=90,
                            end=180,
                            fill="black",
                            width=stroke_width[3])

# Background
draw.ellipse(xy=[(250, 500), (2250, 2500)],
         fill=(205, 127, 50),
         width=5)

# Chin
draw.ellipse(xy=[(1050, 2000), (1450, 2300)], fill=(227, 150, 62))

# Left cheek
distorted_ellipse(draw, (750, 1700), (1250, 2100), (950, 1900), (242, 140, 40), stroke_width=[0, 0, 15, 15])

# Right cheek
distorted_ellipse(draw, (1250, 1700), (1750, 2100), (1550, 1900), (242, 140, 40), stroke_width=[0, 0, 15, 15])

# Left ear
distorted_ellipse(draw, (250, 100), (1050, 1200), (450, 800), (205, 127, 50), quadrants=(True, True, True, True))
# Left ear inside
distorted_ellipse(draw, (350, 200), (750, 800), (450, 600), (184, 115, 51), quadrants=(True, True, True, True))

# Right ear
distorted_ellipse(draw, (1450, 100), (2250, 1200), (2050, 800), (205, 127, 50), quadrants=(True, True, True, True))
# Right ear inside
distorted_ellipse(draw, (1750, 200), (2150, 800), (2050, 600), (184, 115, 51), quadrants=(True, True, True, True))

# Nose
# Upper lip
draw.line(xy=[(1250, 1800), (1250, 1900)], fill=(0, 0, 0), width=15)
# Actual nose
draw.polygon(xy=[(1050, 1600), (1250, 1800), (1450, 1600)], fill=(160, 82, 45))

# Left eye

# Eyes with mask
# Use the mask to set the boundaries of the pupil (black part of eye)
# With a mask, the pupil can get really big without escaping the eyes
# The cat can also squint if it wants to
mask = Image.new("L", (2500, 2500), "white")
draw_mask = ImageDraw.Draw(mask)
# Left eye mask
distorted_ellipse(draw_mask, (650, 1000), (1050, 1400), (750, 1200), "black", quadrants=(True, True, False, False))
distorted_ellipse(draw_mask, (650, 1000), (1050, 1400), (950, 1200), "black", quadrants=(False, False, True, True))
# Right eye mask
distorted_ellipse(draw_mask, (1450, 1000), (1850, 1400), (1750, 1200), "black", quadrants=(True, True, False, False))
distorted_ellipse(draw_mask, (1450, 1000), (1850, 1400), (1550, 1200), "black", quadrants=(False, False, True, True))

eye = Image.new("RGBA", (2500, 2500))
draw_eye = ImageDraw.Draw(eye)
# Left eye
distorted_ellipse(draw_eye, (650, 1000), (1050, 1400), (750, 1200), (9, 121, 105), quadrants=(True, True, False, False))
distorted_ellipse(draw_eye, (650, 1000), (1050, 1400), (950, 1200), (9, 121, 105), quadrants=(False, False, True, True))
draw_eye.ellipse(xy=[(800, 1050), (900, 1350)], fill=(0, 0, 0))
# Right eye
distorted_ellipse(draw_eye, (1450, 1000), (1850, 1400), (1750, 1200), (9, 121, 105), quadrants=(True, True, False, False))
distorted_ellipse(draw_eye, (1450, 1000), (1850, 1400), (1550, 1200), (9, 121, 105), quadrants=(False, False, True, True))
draw_eye.ellipse(xy=[(1600, 1050), (1700, 1350)], fill=(0, 0, 0))

# Perform the composite
image = Image.composite(image, eye, mask)
draw = ImageDraw.Draw(image)

# Save the image for easier git versioning
image.save("cat.png")
