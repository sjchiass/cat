import librosa as lr
import numpy as np
from catlib import *
from tqdm import tqdm

y, sr = lr.load("./second_time_cleaned.mp3", sr=44100)
print(y, sr)
mouth = []
step = sr//20
for s in range(0, len(y), step):
    mouth.append(np.abs(y[s:s+step]).mean())


def cat(ears, mouth):
    layers = [Head(),
              Mouth(),
              LeftCheek(),
              RightCheek(),
              Nose(),
              LeftEar(),
              RightEar(),
              LeftEye(),
              RightEye()]

    # Start a new blank canvas
    image = Image.new("RGB", (500, 500), (0, 255, 0))

    for layer in layers:
        image = (layer
                 .set_mood(openness=15*mouth, turn=ears, dilation=ears)
                 .set_pattern(pattern_name="orange tabby")
                 .draw(image)
                 )

    return image


# frames[0].save("out.gif", save_all=True, append_images=frames[1:], duration=20, loop=0)
for n, (x, y) in enumerate(tqdm(zip(mouth, mouth), total=len(mouth))):
    cat(x, y).convert('RGB').save(f"./frames/{n:05}.jpg")

# ffmpeg -framerate 20 -pattern_type glob -i "./frames/*.jpg" -i second_time_cleaned.mp3 -c:a aac -shortest -c:v libx264 -pix_fmt yuv420p out.mp4 -y
