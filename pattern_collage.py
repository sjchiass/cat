from catlib import *
from PIL import ImageFont

# patterns
layers = [Head(),
       Mouth(),
       LeftCheek(),
       RightCheek(),
       Nose(),
       LeftEar(),
       RightEar(),
       LeftEye(),
       RightEye()
       ]

pattern_collage = Image.new("RGB", (1600, 1600), (255, 255, 255))
font = ImageFont.truetype("DejaVuSans.ttf", 40)

for n, pattern_name in enumerate(Head().pattern_dict.keys()):
    sample = Image.new("RGB", (400, 400), (255, 255, 255))
    for layer in layers:
        sample = layer.set_pattern(pattern_name=pattern_name).draw(sample)
        draw_obj = ImageDraw.Draw(sample)
        draw_obj.text((0, 350), text=pattern_name, fill="red", font=font)
    pattern_collage.paste(sample, (400* (n % 4), 400 * (n // 4)))

pattern_collage.save("pattern_collage.png")
