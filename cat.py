# You are likely to use these libraries
from PIL import Image, ImageDraw
import numpy as np

# Start a new blank canvas
image = Image.new("RGB", (3000, 3500), (255, 255, 255))

# Use the draw object to draw objects
draw = ImageDraw.Draw(image)

# Background
draw.ellipse(xy=[(500, 1500), (2500, 3500)],
         fill=(205, 127, 50),
         width=5)

# Chin
draw.ellipse(xy=[(1300, 3000), (1700, 3200)], fill=(227, 150, 62))

# Left cheek
draw.pieslice(xy=[(1000, 2500), (1700, 3100)],
              start=90,
              end=180,
              fill=(242, 140, 40))
draw.arc(xy=[(1000, 2500), (1700, 3100)],
              start=90,
              end=180,
              fill=(0, 0, 0),
              width=15)

draw.pieslice(xy=[(1100, 2900), (1500, 3100)],
              start=0,
              end=90,
              fill=(242, 140, 40))
draw.arc(xy=[(1100, 2900), (1500, 3100)],
              start=0,
              end=90,
              fill=(0, 0, 0),
              width=15)

draw.pieslice(xy=[(1100, 2800), (1500, 3200)],
              start=270,
              end=0,
              fill=(242, 140, 40))

# Right cheek
draw.pieslice(xy=[(1400, 2500), (2000, 3100)],
              start=0,
              end=90,
              fill=(242, 140, 40))
draw.arc(xy=[(1400, 2500), (2000, 3100)],
              start=0,
              end=90,
              fill=(0, 0, 0),
              width=15)

draw.pieslice(xy=[(1500, 2900), (1900, 3100)],
              start=90,
              end=180,
              fill=(242, 140, 40))
draw.arc(xy=[(1500, 2900), (1900, 3100)],
              start=90,
              end=180,
              fill=(0, 0, 0),
              width=15)

draw.pieslice(xy=[(1500, 2800), (1900, 3200)],
              start=180,
              end=270,
              fill=(242, 140, 40))

# Nose
# Upper lip
draw.line(xy=[(1500, 2800), (1500, 3000)], fill=(0, 0, 0), width=15)
# Actual nose
draw.polygon(xy=[(1300, 2600), (1500, 2800), (1700, 2600)], fill=(160, 82, 45))

# Left eye
draw.ellipse(xy=[(900, 2000), (1300, 2400)], fill=(9, 121, 105))
# Left pupil
draw.ellipse(xy=[(1050, 2100), (1150, 2300)], fill=(0, 0, 0))

# Right eye
draw.ellipse(xy=[(1700, 2000), (2100, 2400)], fill=(9, 121, 105))
# Right pupil
draw.ellipse(xy=[(1850, 2100), (1950, 2300)], fill=(0, 0, 0))

# Left ear
draw.rounded_rectangle(xy=[(500, 1300), (1200, 2000)], radius=500, fill=(205, 127, 50))
draw.rectangle(xy=[(500, 1300), (850, 1650)], fill=(205, 127, 50))

# Right ear
draw.rounded_rectangle(xy=[(1800, 1300), (2500, 2000)], radius=500, fill=(205, 127, 50))
draw.rectangle(xy=[(2150, 1300), (2500, 1650)], fill=(205, 127, 50))


# In Jupyter, this will display the image
image.show()
