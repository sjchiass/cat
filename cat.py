from catlib import *

cat0 = [Head(),
       Mouth(),
       LeftCheek(),
       RightCheek(),
       Nose(),
       LeftEar(),
       RightEar(),
       LeftEye(),
       RightEye(),
       LeftWhisker(),
       RightWhisker(),
       LeftEyebrow(),
       RightEyebrow()
       ]


# Start a new blank canvas
image = Image.new("RGB", (2500, 2500), (255, 255, 255))

for x in cat0:
    image = x.set_pattern("orange").draw(image)

# Save the image for easier git versioning
image.save("cat.png")

cat1 = [Head(),
       Mouth(),
       LeftCheek(),
       RightCheek(),
       Nose(),
       LeftEar(),
       RightEar(),
       LeftEye(),
       RightEye(),
       LeftWhisker(),
       RightWhisker(),
       LeftEyebrow(),
       RightEyebrow()]

cat2= [Head(),
       Mouth(),
       LeftCheek(),
       RightCheek(),
       Nose(),
       LeftEar(),
       RightEar(),
       LeftEye(),
       RightEye(),
       LeftWhisker(),
       RightWhisker(),
       LeftEyebrow(),
       RightEyebrow()]

cat3= [Head(width=1.25),
       Mouth(),
       LeftCheek(),
       RightCheek(),
       Nose(),
       LeftEar(),
       RightEar(),
       LeftEye(),
       RightEye(),
       LeftWhisker(),
       RightWhisker(),
       LeftEyebrow(),
       RightEyebrow()]

images = [
    Image.new("RGB", (2500, 2500), (255, 255, 255)),
    Image.new("RGB", (2500, 2500), (255, 255, 255)),
    Image.new("RGB", (2500, 2500), (255, 255, 255)),
    Image.new("RGB", (2500, 2500), (255, 255, 255))
]

for x in cat0:
    images[0] = x.set_pattern("orange").set_mood("neutral").draw(images[0])
for x in cat1:
    images[1] = x.set_pattern("orange").set_mood(["neutral", "angry"]).draw(images[1])
for x in cat2:
    images[2] = x.set_pattern("orange").set_mood("angry").draw(images[2])
for x in cat3:
    images[3] = x.set_pattern("orange").set_mood("excited", openness=0.2, turn=0.0).draw(images[3])

images = [i.resize((250, 250)) for i in images]

collage = Image.new("RGB", (500, 500), (255, 255, 255))
collage.paste(images[0], (0, 0))
collage.paste(images[1], (250, 0))
collage.paste(images[2], (0, 250))
collage.paste(images[3], (250, 250))

collage.save("collage.png")
