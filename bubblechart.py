import pandas as pd
from pydataset import data
from PIL import ImageFont

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

# xlim and ylim
xlim = max(df.iloc[:,0])*1.1
ylim = max(df.iloc[:,1])*1.1
alim = max(df.iloc[:,2])

def draw_datapoint(im, x, y, a, pattern):
    im = im.copy()
    marker = Image.new("RGBA", (int(im.width/10*a/alim), int(im.height/10*a/alim)), (255, 0, 0, 0))
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
             [int((im.width*x/xlim)-(im.width/20*a/alim)),
              int((im.height-im.height*y/ylim)-(im.height/20*a/alim))],
              marker)
    return im

graphing_area = Image.new("RGBA", (1500, 1500), (255, 0, 0, 0))

for index, row in df.iterrows():
    graphing_area = draw_datapoint(graphing_area,
                           row["hp"],
                           row["qsec"],
                           row["disp"],
                           markers[row["cyl"]])

font = ImageFont.truetype("DejaVuSans.ttf", 40)

image = Image.new("RGBA", (2500, 2500), (255, 255, 255))
draw_obj = ImageDraw.Draw(image)

draw_obj.line([(500, 500), (500, 2000), (2000, 2000)], "black", 5)
draw_obj.polygon([(475, 500), (525, 500), (500, 475)], "black")
draw_obj.polygon([(2000, 1975), (2000, 2025), (2025, 2000)], "black")
draw_obj.text((1250, 2100), text="hp", fill="red", font=font)
v = Image.new("RGBA", (500, 500), (255, 0, 0, 0))
v_draw = ImageDraw.Draw(v)
_, _, w, h = v_draw.textbbox((0, 0), "qsec", font=font)
v_draw.text(((500-w)/2, (500-h)/2), text="qsec", fill="red", font=font)
v = v.rotate(90, center=(250, 250))
image.paste(v, (150, 1000), v)
image.paste(graphing_area, (500, 500), graphing_area)

# Legend
for n, (k, v) in enumerate(markers.items()):
    marker = Image.new("RGBA", (100, 100), (255, 0, 0, 0))
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
        marker = layer.set_pattern(v).draw(marker)
    image.paste(marker,
             (2150, 650+n*200),
              marker)
    draw_obj.text((2150, 750+n*200), text=k, fill="red", font=font)

image.save("bubblechart.png")
