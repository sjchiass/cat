import pandas as pd
import numpy as np
from pydataset import data
from PIL import ImageFont
from catlib import *

class BubbleChart():
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
    @staticmethod
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
    @staticmethod
    def round_to_1(x, max):
        return int(round(x, -int(math.floor(math.log10(abs(max))))))

    # Drawing a datapoint is creating a small cat image and pasting it
    # in the right place
    def draw_datapoint(self, im, xmin, xmax, ymin, ymax, amax, W, H, x, y, a, pattern):
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
            
        im.paste(marker, self.graph_space_projection((W//5, H//5), (3*W//5, 3*H//5), (xmin, xmax), (ymin, ymax), (x, y), marker.size), marker)
        return im

    def __init__(self, x, y, a, m, p, x_label, y_label, a_label, m_label, title, W, H):
        m = [str(m) for m in m]

        markers = dict()
        m_list = np.unique(m)
        for marker, pattern in zip(m_list, p):
            markers[marker] = pattern

        # xmax and ymax
        # Here I start at 0 and go 10% above the real max
        xmin = 0
        xmax = max(x)*1.1
        ymin = 0
        ymax = max(y)*1.1
        amax = max(a)

        image = Image.new("RGBA", (W, H), (255, 255, 255))

        for _x, _y, _a, _m in zip(x, y, a, m):
            image = self.draw_datapoint(image, xmin, xmax, ymin, ymax, amax, W, H, _x, _y, _a, markers[_m])

        font = ImageFont.truetype("DejaVuSans.ttf", (W+H)//100)
        draw_obj = ImageDraw.Draw(image)

        # Axes
        draw_obj.line([(W//5, H//5), (W//5, 4*H//5), (4*W//5, 4*H//5)], "black", (W+H)//1000)
        draw_obj.polygon([(W//5 - W//100, H//5),
                        (W//5 + W//100, H//5),
                        (W//5, H//5 - H//100)], "black")
        draw_obj.polygon([(4*W//5, 4*H//5 - H//100),
                        (4*W//5, 4*H//5 + H//100),
                        (4*W//5 + H//100, 4*H//5)], "black")
        _, _, w, h = draw_obj.textbbox((0, 0), x_label, font=font)
        draw_obj.text((W//2 - w/2, 4*H//5 + H//25 -h/2),
                    text=x_label, fill="black", font=font)
        # Vertical text
        v = Image.new("RGBA", (W//5, H//5), (255, 0, 0, 0))
        v_draw = ImageDraw.Draw(v)
        _, _, w, h = v_draw.textbbox((0, 0), y_label, font=font)
        v_draw.text(((W//5-w)/2, (H//5-h)/2), text=y_label, fill="black", font=font)
        v = v.rotate(90, center=(W//10, H//10))
        image.paste(v, (2*W//50, 2*H//5), v)

        # Ticks
        xticks = [self.round_to_1(xt*xmax/5, xmax) for xt in range(5)]
        for xt in xticks:
            # Determine text box size
            _, _, w, h = draw_obj.textbbox((0, 0), str(xt), font=font)
            t = Image.new("RGBA", (w, h), (255, 0, 0, 0))
            t_draw = ImageDraw.Draw(t)
            t_draw.text((0, 0), text=str(xt), fill="black", font=font)
            image.paste(t, self.graph_space_projection((W//5, H//5), (3*W//5, 3*H//5), (xmin, xmax), (ymin, ymax), (xt, 0), t.size, (0, t.height//2)), t)
        yticks = [self.round_to_1(yt*ymax/5, ymax) for yt in range(5)]
        for yt in yticks:
            # Determine text box size
            _, _, w, h = draw_obj.textbbox((0, 0), str(yt), font=font)
            t = Image.new("RGBA", (w, h), (255, 0, 0, 0))
            t_draw = ImageDraw.Draw(t)
            t_draw.text((0, 0), text=str(yt), fill="black", font=font)
            image.paste(t, self.graph_space_projection((W//5, H//5), (3*W//5, 3*H//5), (xmin, xmax), (ymin, ymax), (0, yt), t.size, (-t.width//2, 0)), t)

        # Legend
        _, _, w, h = draw_obj.textbbox((0, 0), "legend", font=font)
        draw_obj.text((4*W//5 + W//10 - w/2, H//5 + H//50 - h/2), text="legend", fill="black", font=font)
        for n, (k, v) in enumerate(markers.items()):
            marker = Image.new("RGBA", (W//25, H//25), (255, 0, 0, 0))
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
                    (4*W//5 + 4*W//50, H//5 + 3*H//50 + n*4*H//50),
                    marker)
            _, _, w, h = draw_obj.textbbox((0, 0), f"{k} {m_label}", font=font)
            draw_obj.text((4*W//5 + W//10 - w/2, 3*H//10 + n*4*H//50 - h/2), text=f"{k} {m_label}", fill="black", font=font)

        # Title
        _, _, w, h = draw_obj.textbbox((0, 0), title, font=font)
        draw_obj.text((W//2 - w/2, H//10 - h/2), text=title, fill="black", font=font)

        image.save("bubblechart.png")

df = (
    data("mtcars")
    [["hp", "disp", "mpg", "cyl"]]
    .sort_values("mpg", ascending=False)
    )

BubbleChart(
    x = df.hp.tolist(),
    y = df.disp.tolist(),
    a = df.mpg.tolist(),
    m = df.cyl.tolist(),
    p = ["orange tabby", "grey tabby", "calico"],
    x_label = "horsepower",
    y_label = "displacement",
    a_label = "",
    m_label = "cylinders",
    title = "mtcars: horsepower vs. displacement",
    W = 500,
    H = 500)
