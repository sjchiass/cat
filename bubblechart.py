import pandas as pd
from pydataset import data
from PIL import ImageFont

df = (
    data("mtcars")
    [["hp", "disp", "mpg", "cyl"]]
    .sort_values("mpg", ascending=False)
    )
df.cyl = df.cyl.astype(str)

from catlib import *

markers = dict()
for n, i in enumerate(list(df.cyl.drop_duplicates().values)):
    markers[i] = ["orange tabby", "grey tabby", "calico"][n]

# xmax and ymax
# Here I start at 0 and go 10% above the real max
xmin = 0
xmax = max(df.iloc[:,0])*1.1
ymin = 0
ymax = max(df.iloc[:,1])*1.1
amax = max(df.iloc[:,2])

# When it comes to drawing point on the graph space, it's necessary
# to transform x, y data coordinates to coordinates in the image.
# On top of that, the graphing space itself might move around the 
# image, so offsets are also needed. Finally, the final coordinates
# also need to be adjusted a little to account for the marker's size.
# Last of all, this function must also help with drawing axis ticks, 
# which have to be nudged a little outside the graphing space. So
# another set of offsets are needed.
#
# Helpful note: pillow's y axis is inverted from the usual cartesian
# space we're used to. x=0, y=0 is at the top of the image. Our graph
# though has the usual y (so it has to be flipped).
def graph_space_projection(graph_space_xy, graph_space_size, x_range, y_range, data_xy, marker_size, adj_xy=(0, 0)):
    if data_xy[0] < x_range[0] or data_xy[0] > x_range[1]:
        raise ValueError(f"x value {data_xy[0]} outside {x_range}")
    elif data_xy[1] < y_range[0] or data_xy[1] > y_range[1]:
        raise ValueError(f"y value {data_xy[1]} outside {y_range}")
    return [int(adj_xy[0]+graph_space_xy[0]
                +graph_space_size[0]
                  *(data_xy[0]-x_range[0])/(x_range[1]-x_range[0])
                  -marker_size[0]/2),
                  int(adj_xy[1]+graph_space_xy[1]
                      +graph_space_size[1]*(1-(data_xy[1]-y_range[0])/(y_range[1]-y_range[0]))
                        -marker_size[1]/2)]

# https://stackoverflow.com/a/3411435
# When figuring out the ticks, a cheap way is to take the maximum
# values and print their nearby units of 10s. So 450 would have
# 400, 300, 200, 100, 0. 75 would have 70, 60, 50, ...
def round_to_1(x, max):
    return int(round(x, -int(math.floor(math.log10(abs(max))))))

# Drawing a datapoint is creating a small cat image and pasting it
# in the right place
def draw_datapoint(im, x, y, a, pattern):
    im = im.copy()
    # Data values affect marker area, so a data point 25% the value
    # of another is 50% its width and 50% is height.
    marker = Image.new("RGBA",
                       (int(im.width/10*math.sqrt(a/amax)),
                        int(im.height/10*math.sqrt(a/amax))),
                        (255, 0, 0, 0))
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
        
    im.paste(marker, graph_space_projection((500, 500), (1500, 1500), (xmin, xmax), (ymin, ymax), (x, y), marker.size), marker)
    return im

image = Image.new("RGBA", (2500, 2500), (255, 255, 255))

for index, row in df.iterrows():
    image = draw_datapoint(image,
                           row["hp"],
                           row["disp"],
                           row["mpg"],
                           markers[row["cyl"]])

font = ImageFont.truetype("DejaVuSans.ttf", 40)
draw_obj = ImageDraw.Draw(image)

# Axes
draw_obj.line([(500, 500), (500, 2000), (2000, 2000)], "black", 5)
draw_obj.polygon([(475, 500), (525, 500), (500, 475)], "black")
draw_obj.polygon([(2000, 1975), (2000, 2025), (2025, 2000)], "black")
_, _, w, h = draw_obj.textbbox((0, 0), "hp", font=font)
draw_obj.text((1250-w/2, 2100-h/2), text="hp", fill="black", font=font)
# Vertical text
v = Image.new("RGBA", (500, 500), (255, 0, 0, 0))
v_draw = ImageDraw.Draw(v)
_, _, w, h = v_draw.textbbox((0, 0), "disp", font=font)
v_draw.text(((500-w)/2, (500-h)/2), text="disp", fill="black", font=font)
v = v.rotate(90, center=(250, 250))
image.paste(v, (150, 1000), v)

# Ticks
xticks = [round_to_1(x*xmax/5, xmax) for x in range(5)]
for x in xticks:
    # Determine text box size
    _, _, w, h = draw_obj.textbbox((0, 0), str(x), font=font)
    t = Image.new("RGBA", (w, h), (255, 0, 0, 0))
    t_draw = ImageDraw.Draw(t)
    t_draw.text((0, 0), text=str(x), fill="black", font=font)
    image.paste(t, graph_space_projection((500, 500), (1500, 1500), (xmin, xmax), (ymin, ymax), (x, 0), t.size, (0, 50)), t)
yticks = [round_to_1(y*ymax/5, ymax) for y in range(5)]
for y in yticks:
    # Determine text box size
    _, _, w, h = draw_obj.textbbox((0, 0), str(y), font=font)
    t = Image.new("RGBA", (w, h), (255, 0, 0, 0))
    t_draw = ImageDraw.Draw(t)
    t_draw.text((0, 0), text=str(y), fill="black", font=font)
    image.paste(t, graph_space_projection((500, 500), (1500, 1500), (xmin, xmax), (ymin, ymax), (0, y), t.size, (-50, 0)), t)
    

# Legend
_, _, w, h = draw_obj.textbbox((0, 0), "legend", font=font)
draw_obj.text((2250-w/2, 550-h/2), text="legend", fill="black", font=font)
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
             (2200, 650+n*200),
              marker)
    _, _, w, h = draw_obj.textbbox((0, 0), k+" cyl", font=font)
    draw_obj.text((2250-w/2, 750+n*200-h/2), text=k+" cyl", fill="black", font=font)

# Title
_, _, w, h = draw_obj.textbbox((0, 0), "mtcars: horsepower vs. displacement", font=font)
draw_obj.text((1250-w/2, 250-h/2), text="mtcars: horsepower vs. displacement", fill="black", font=font)

image.save("bubblechart.png")
