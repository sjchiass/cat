from catlib import *

cat0 = [Head(),
       Mouth(),
       LeftCheek(),
       RightCheek(),
       Nose(),
       LeftEar(),
       RightEar(),
       LeftEye(),
       RightEye()]


# Start a new blank canvas
image = Image.new("RGB", (2500, 2500), (255, 255, 255))

for x in cat0:
    image = x.draw(image)

# Save the image for easier git versioning
image.save("cat.png")

cat1 = [Head(),
       Mouth(openness=0.5),
       LeftCheek(width=1.2),
       RightCheek(width=1.2),
       Nose(),
       LeftEar(turn=0.5),
       RightEar(turn=0.5),
       LeftEye(eye_height=0.5),
       RightEye(eye_height=0.5)]

cat2= [Head(),
       Mouth(openness=1.0),
       LeftCheek(width=1.35),
       RightCheek(width=1.35),
       Nose(),
       LeftEar(turn=1.0),
       RightEar(turn=1.0),
       LeftEye(eye_height=0.2),
       RightEye(eye_height=0.2)]

cat3= [Head(width=1.25),
       Mouth(openness=0.2),
       LeftCheek(width=0.8),
       RightCheek(width=0.8),
       Nose(),
       LeftEar(),
       RightEar(),
       LeftEye(pupil_width=4, pupil_height=1.25),
       RightEye(pupil_width=4, pupil_height=1.25)]

images = [
    Image.new("RGB", (2500, 2500), (255, 255, 255)),
    Image.new("RGB", (2500, 2500), (255, 255, 255)),
    Image.new("RGB", (2500, 2500), (255, 255, 255)),
    Image.new("RGB", (2500, 2500), (255, 255, 255))
]

for x in cat0:
    images[0] = x.draw(images[0])
for x in cat1:
    images[1] = x.draw(images[1])
for x in cat2:
    images[2] = x.draw(images[2])
for x in cat3:
    images[3] = x.draw(images[3])

images = [i.resize((250, 250)) for i in images]

collage = Image.new("RGB", (500, 500), (255, 255, 255))
collage.paste(images[0], (0, 0))
collage.paste(images[1], (250, 0))
collage.paste(images[2], (0, 250))
collage.paste(images[3], (250, 250))

collage.save("collage.png")
