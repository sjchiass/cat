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
    def draw_datapoint(self, im, x, y, a, pattern):
        im = im.copy()
        # Data values affect marker area, so a data point 25% the value
        # of another is 50% its width and 50% is height.
        marker = Image.new("RGBA",
                        (int(im.width/10*math.sqrt(a/self.amax)),
                            int(im.height/10*math.sqrt(a/self.amax))),
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
            
        im.paste(marker, self.graph_space_projection((self.W//5, self.H//5),
                                                     (3*self.W//5, 3*self.H//5),
                                                     (self.xmin, self.xmax),
                                                     (self.ymin, self.ymax),
                                                     (x, y),
                                                     marker.size), marker)
        return im

    def __init__(self, x, y, a, m, p, x_label, y_label, a_label, m_label, title, W, H):
        self.x = x
        self.y = y
        self.a = a
        self.m = m
        self.p = p
        self.x_label = x_label
        self.y_label = y_label
        self.a_label = a_label
        self.m_label = m_label
        self.title = title
        self.W = W
        self.H = H

        self.m = [str(m) for m in self.m]

        self.markers = dict()
        m_list = np.unique(self.m)
        for marker, pattern in zip(m_list, self.p):
            self.markers[marker] = pattern

        # xmax and ymax
        # Here I start at 0 and go 10% above the real max
        self.xmin = 0
        self.xmax = max(x)*1.1
        self.ymin = 0
        self.ymax = max(y)*1.1
        self.amax = max(a)

        self.image = Image.new("RGBA", (W, H), (255, 255, 255))
        
        self.data()
        self.axes()
        self.legend()

    def image(self):
        return self.image

    def data(self):
        # Draw data
        for _x, _y, _a, _m in zip(self.x, self.y, self.a, self.m):
            self.image = self.draw_datapoint(self.image, _x, _y, _a, self.markers[_m])

    def axes(self):
        font = ImageFont.truetype("DejaVuSans.ttf", (self.W+self.H)//100)
        draw_obj = ImageDraw.Draw(self.image)

        # Axes
        draw_obj.line([(self.W//5, self.H//5), (self.W//5, 4*self.H//5), (4*self.W//5, 4*self.H//5)], "black", (self.W+self.H)//1000)
        draw_obj.polygon([(self.W//5 - self.W//100, self.H//5),
                        (self.W//5 + self.W//100, self.H//5),
                        (self.W//5, self.H//5 - self.H//100)], "black")
        draw_obj.polygon([(4*self.W//5, 4*self.H//5 - self.H//100),
                        (4*self.W//5, 4*self.H//5 + self.H//100),
                        (4*self.W//5 + self.H//100, 4*self.H//5)], "black")
        _, _, w, h = draw_obj.textbbox((0, 0), self.x_label, font=font)
        draw_obj.text((self.W//2 - w/2, 4*self.H//5 + self.H//25 -h/2),
                    text=self.x_label, fill="black", font=font)
        # Vertical text
        v = Image.new("RGBA", (self.W//5, self.H//5), (255, 0, 0, 0))
        v_draw = ImageDraw.Draw(v)
        _, _, w, h = v_draw.textbbox((0, 0), self.y_label, font=font)
        v_draw.text(((self.W//5-w)/2, (self.H//5-h)/2), text=self.y_label, fill="black", font=font)
        v = v.rotate(90, center=(self.W//10, self.H//10))
        self.image.paste(v, (2*self.W//50, 2*self.H//5), v)

        # Ticks
        xticks = [self.round_to_1(xt*self.xmax/5, self.xmax) for xt in range(5)]
        for xt in xticks:
            # Determine text box size
            _, _, w, h = draw_obj.textbbox((0, 0), str(xt), font=font)
            t = Image.new("RGBA", (w, h), (255, 0, 0, 0))
            t_draw = ImageDraw.Draw(t)
            t_draw.text((0, 0), text=str(xt), fill="black", font=font)
            self.image.paste(t, self.graph_space_projection((self.W//5, self.H//5),
                                                            (3*self.W//5, 3*self.H//5),
                                                            (self.xmin, self.xmax),
                                                            (self.ymin, self.ymax),
                                                            (xt, 0),
                                                            t.size,
                                                            (0, t.height//2)), t)
        yticks = [self.round_to_1(yt*self.ymax/5, self.ymax) for yt in range(5)]
        for yt in yticks:
            # Determine text box size
            _, _, w, h = draw_obj.textbbox((0, 0), str(yt), font=font)
            t = Image.new("RGBA", (w, h), (255, 0, 0, 0))
            t_draw = ImageDraw.Draw(t)
            t_draw.text((0, 0), text=str(yt), fill="black", font=font)
            self.image.paste(t, self.graph_space_projection((self.W//5, self.H//5),
                                                            (3*self.W//5, 3*self.H//5),
                                                            (self.xmin, self.xmax), (self.ymin, self.ymax),
                                                            (0, yt),
                                                            t.size,
                                                            (-t.width//2, 0)), t)

    def legend(self):
        font = ImageFont.truetype("DejaVuSans.ttf", (self.W+self.H)//100)
        draw_obj = ImageDraw.Draw(self.image)

        # Legend
        _, _, w, h = draw_obj.textbbox((0, 0), "legend", font=font)
        draw_obj.text((4*self.W//5 + self.W//10 - w/2, self.H//5 + self.H//50 - h/2), text="legend", fill="black", font=font)
        for n, (k, v) in enumerate(self.markers.items()):
            marker = Image.new("RGBA", (self.W//25, self.H//25), (255, 0, 0, 0))
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
            self.image.paste(marker,
                    (4*self.W//5 + 4*self.W//50, self.H//5 + 3*self.H//50 + n*4*self.H//50),
                    marker)
            _, _, w, h = draw_obj.textbbox((0, 0), f"{k} {self.m_label}", font=font)
            draw_obj.text((4*self.W//5 + self.W//10 - w/2, 3*self.H//10 + n*4*self.H//50 - h/2), text=f"{k} {self.m_label}", fill="black", font=font)

        # Title
        _, _, w, h = draw_obj.textbbox((0, 0), self.title, font=font)
        draw_obj.text((self.W//2 - w/2, self.H//10 - h/2), text=self.title, fill="black", font=font)

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
    H = 500).image.save("bubblechart.png")

df = (
    data("mtcars")
    .corr()
)

class HeatMap(BubbleChart):
    def __init__(self,
                 XY,
                 x_label,
                 y_label,
                 m_lim,
                 moods,
                 pattern, 
                 title,
                 W,
                 H):
        self.XY = XY
        self.x_label = x_label
        self.y_label = y_label
        self.m_lim = m_lim
        self.moods = moods
        self.pattern = pattern
        self.title = title
        self.W = W
        self.H = H

        self.x_label = [str(x_label) for x_label in self.x_label]
        self.y_label = [str(y_label) for y_label in self.y_label]

        self.image = Image.new("RGBA", (W, H), (255, 255, 255))
        
        self.data()
        self.axes()
        # self.legend()
    
    def data(self):
        # Draw data
        for _x in range(self.XY.shape[1]):
            for _y in range(self.XY.shape[0]):
                if self.XY[_x, _y] < 0:
                    mood = {"scared" : -self.XY[_x, _y]}
                else:
                    mood = {"angry" : self.XY[_x, _y]}
                self.image = self.draw_datapoint(self.image, _x, _y, self.XY.shape[1], self.XY.shape[0], mood)

    # Drawing a datapoint is creating a small cat image and pasting it
    # in the right place
    def draw_datapoint(self, im, x, y, xmax, ymax, mood):
        im = im.copy()
        # Data values affect marker area, so a data point 25% the value
        # of another is 50% its width and 50% is height.
        marker = Image.new("RGBA", (3*self.W//5//xmax, 3*self.H//5//ymax), (255, 0, 0, 0))
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
            marker = layer.set_pattern(self.pattern).set_mood(mood).draw(marker)
            
        im.paste(marker, (self.W//5 + x*3*self.W//5//xmax,
                          self.H//5 + y*3*self.H//5//ymax), marker)
        return im

    def axes(self):
        font = ImageFont.truetype("DejaVuSans.ttf", (self.W+self.H)//100)
        draw_obj = ImageDraw.Draw(self.image)

        # Axes
        draw_obj.line([(self.W//5, self.H//5),
                       (self.W//5, 4*self.H//5),
                       (4*self.W//5, 4*self.H//5),
                       (4*self.W//5, self.H//5),
                       (self.W//5, self.H//5)],
                       "black", (self.W+self.H)//1000)

        # Ticks
        xmax = len(self.x_label)
        ymax = len(self.y_label)
        for n, xt in enumerate(self.x_label):
            # Determine text box size
            _, _, w, h = draw_obj.textbbox((0, 0), str(xt), font=font)
            t = Image.new("RGBA", (w, h), (255, 0, 0, 0))
            t_draw = ImageDraw.Draw(t)
            t_draw.text((0, 0), text=str(xt), fill="black", font=font)
            self.image.paste(t,
                             (self.W//5 + n*3*self.W//5//xmax,
                              self.H//5 - h),
                              t)
            self.image.paste(t,
                             (self.W//5 + n*3*self.W//5//xmax,
                              4*self.H//5),
                              t)
        
        for n, yt in enumerate(self.y_label):
            # Determine text box size
            _, _, w, h = draw_obj.textbbox((0, 0), str(yt), font=font)
            t = Image.new("RGBA", (w, h), (255, 0, 0, 0))
            t_draw = ImageDraw.Draw(t)
            t_draw.text((0, 0), text=str(yt), fill="black", font=font)
            self.image.paste(t,
                             (self.W//5 - w,
                              self.H//5 + n*3*self.H//5//ymax + h),
                              t)
            self.image.paste(t,
                             (4*self.W//5,
                              self.H//5 + n*3*self.H//5//ymax + h),
                              t)

HeatMap(XY=df.values,
        x_label=df.index,
        y_label=df.columns,
        m_lim=[-1, 1],
        moods=["scared", "neutral", "angry"],
        pattern="orange tabby",
        title="Correlation of mtcars",
        W=2500,
        H=2500).image.save("heatmap.png")
