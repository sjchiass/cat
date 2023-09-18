# You are likely to use these libraries
from PIL import Image, ImageDraw
import numpy as np

# Start a new blank canvas
image = Image.new("RGB", (3000, 3500), (255, 255, 255))

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
draw.ellipse(xy=[(500, 1500), (2500, 3500)],
         fill=(205, 127, 50),
         width=5)

# Chin
draw.ellipse(xy=[(1300, 3000), (1700, 3300)], fill=(227, 150, 62))

# Left cheek
distorted_ellipse(draw, (1000, 2700), (1500, 3100), (1200, 2900), (242, 140, 40), stroke_width=[0, 0, 15, 15])

# Right cheek
distorted_ellipse(draw, (1500, 2700), (2000, 3100), (1800, 2900), (242, 140, 40), stroke_width=[0, 0, 15, 15])

# Left ear
distorted_ellipse(draw, (500, 1100), (1300, 2200), (700, 1800), (205, 127, 50), quadrants=(True, True, True, True))
# Left ear inside
distorted_ellipse(draw, (600, 1200), (1000, 1800), (700, 1600), (184, 115, 51), quadrants=(True, True, True, True))

# Right ear
distorted_ellipse(draw, (1700, 1100), (2500, 2200), (2300, 1800), (205, 127, 50), quadrants=(True, True, True, True))
# Right ear inside
distorted_ellipse(draw, (2000, 1200), (2400, 1800), (2300, 1600), (184, 115, 51), quadrants=(True, True, True, True))

# Nose
# Upper lip
draw.line(xy=[(1500, 2800), (1500, 2900)], fill=(0, 0, 0), width=15)
# Actual nose
draw.polygon(xy=[(1300, 2600), (1500, 2800), (1700, 2600)], fill=(160, 82, 45))

# Left eye

# Eyes with mask
# Use the mask to set the boundaries of the pupil (black part of eye)
# With a mask, the pupil can get really big without escaping the eyes
# The cat can also squint if it wants to
mask = Image.new("L", (3000, 3500), "white")
draw_mask = ImageDraw.Draw(mask)
# Left eye mask
distorted_ellipse(draw_mask, (900, 2000), (1300, 2400), (1000, 2200), "black", quadrants=(True, True, False, False))
distorted_ellipse(draw_mask, (900, 2000), (1300, 2400), (1200, 2200), "black", quadrants=(False, False, True, True))
# Right eye mask
distorted_ellipse(draw_mask, (1700, 2000), (2100, 2400), (2000, 2200), "black", quadrants=(True, True, False, False))
distorted_ellipse(draw_mask, (1700, 2000), (2100, 2400), (1800, 2200), "black", quadrants=(False, False, True, True))

eye = Image.new("RGBA", (3000, 3500))
draw_eye = ImageDraw.Draw(eye)
# Left eye
distorted_ellipse(draw_eye, (900, 2000), (1300, 2400), (1000, 2200), (9, 121, 105), quadrants=(True, True, False, False))
distorted_ellipse(draw_eye, (900, 2000), (1300, 2400), (1200, 2200), (9, 121, 105), quadrants=(False, False, True, True))
draw_eye.ellipse(xy=[(1050, 2050), (1150, 2350)], fill=(0, 0, 0))
# Right eye
distorted_ellipse(draw_eye, (1700, 2000), (2100, 2400), (2000, 2200), (9, 121, 105), quadrants=(True, True, False, False))
distorted_ellipse(draw_eye, (1700, 2000), (2100, 2400), (1800, 2200), (9, 121, 105), quadrants=(False, False, True, True))
draw_eye.ellipse(xy=[(1850, 2050), (1950, 2350)], fill=(0, 0, 0))

# Perform the composite
image = Image.composite(image, eye, mask)
draw = ImageDraw.Draw(image)

# Save the image for easier git versioning
image.save("cat.png")
