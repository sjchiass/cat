from catlib import *
from PIL import ImageFont

# moods
layers = [Head(),
       Mouth(),
       LeftCheek(),
       RightCheek(),
       Nose(),
       LeftEar(),
       RightEar(),
       LeftEye(),
       RightEye(),
       LeftWhisker(thickness=5),
       RightWhisker(thickness=5)
       ]

mood_collage = Image.new("RGB", (1600, 1600), (255, 255, 255))
font = ImageFont.truetype("DejaVuSans.ttf", 40)

for n, mood_name in enumerate(Head().mood_dict.keys()):
    sample = Image.new("RGB", (400, 400), (255, 255, 255))
    for layer in layers:
        sample = layer.set_mood(mood_name=mood_name).draw(sample)
        draw_obj = ImageDraw.Draw(sample)
        draw_obj.text((0, 350), text=mood_name, fill="red", font=font)
    mood_collage.paste(sample, (400* (n % 4), 400 * (n // 4)))

mood_collage.save("mood_collage.png")
