import pandas as pd
from pydataset import data

df = (
    data("mtcars")
    [["hp", "qsec", "disp", "cyl"]]
    .sort_values("disp", ascending=False)
    )
df.cyl = df.cyl.astype(str)

from catlib import *

markers = dict()
for n, i in enumerate(list(df.cyl.drop_duplicates().values)):
    markers[i] = ["orange tabby", "grey tabby", "calico"][n]

print(markers)

# xlim and ylim
xlim = max(df.iloc[:,0])*1.1
ylim = max(df.iloc[:,1])*1.1
alim = max(df.iloc[:,2])
print(xlim, ylim, alim)

def draw_datapoint(im, x, y, a, pattern):
    im = im.copy()
    marker = Image.new("RGBA", (int(250*a/alim), int(250*a/alim)), (255, 0, 0, 0))
    cat = [Head(),
        Mouth(),
        LeftCheek(),
        RightCheek(),
        Nose(),
        LeftEar(),
        RightEar(),
        LeftEye(),
        RightEye()
        ]
    for layer in cat:
        marker = layer.set_pattern(pattern).draw(marker)
    im.paste(marker,
             [int((2500*x/xlim)-(125*a/alim)),
              int((2500-2500*y/ylim)-(125*a/alim))],
              marker)
    return im

image = Image.new("RGBA", (2500, 2500), (255, 255, 255))

for index, row in df.iterrows():
    image = draw_datapoint(image,
                           row["hp"],
                           row["qsec"],
                           row["disp"],
                           markers[row["cyl"]])

image.save("bubblechart.png")
