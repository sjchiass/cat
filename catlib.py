import math
import random
from PIL import Image, ImageDraw, ImageEnhance

# Base class full of methods and other data
class Cat:
    # The canvas size the layers were designed in.
    # The actual output images are rescaled from this design size
    # to the actual size of the image being drawn.
    __ref_width = 2500
    __ref_height = 2500
    pattern_dict = {
        "orange" : {"fill" : (205, 127, 50),
                    "nose" : (160, 82, 45),
                    "white_neck" : False,
                    "spots" : None,
                    "tabby" : None},
        "orange tabby" : {"fill" : (205, 127, 50),
                    "nose" : (255, 167, 166),
                    "white_neck" : True,
                    "spots" : None,
                    "tabby" : (160, 73, 30)},
        "tuxedo" : {"fill" : (32, 32, 36),
                          "nose" : "black",
                    "white_neck" : True,
                    "spots" : None,
                    "tabby" : None},
        "black" : {"fill" : (32, 32, 36),
                          "nose" : "black",
                    "white_neck" : False,
                    "spots" : None,
                    "tabby" : None},
        "grey tabby" : {"fill" : "grey",
                    "nose" : (160, 82, 45),
                    "white_neck" : True,
                    "spots" : None,
                    "tabby" : (64, 64, 64)},
        "russian blue" : {"fill" : (102, 109, 113),
                          "nose" : (25, 30, 32),
                    "white_neck" : False,
                    "spots" : None,
                    "tabby" : None},
        "calico" : {"fill" : (32, 32, 36),
                    "nose" : (160, 82, 45),
                    "white_neck" : True,
                    "spots" : [(205, 127, 50), (160, 73, 30)],
                    "tabby" : None},
        "calico_spots" : {"fill" : "white",
                    "nose" : (255, 167, 166),
                    "white_neck" : False,
                    "spots" : [(205, 127, 50), (160, 73, 30), (32, 32, 36)],
                    "tabby" : None},
        "tortoiseshell" : {"fill" : (32, 32, 36),
                    "nose" : "black",
                    "white_neck" : False,
                    "spots" : [(205, 127, 50), (160, 73, 30)],
                    "tabby" : None}
    }
    mood_dict = {
        "neutral" : {
            "openness" : 0.0,
            "turn" : 0.0,
            "squint" : 0.25,
            "dilation" : 0.1,
            "droopiness" : 0.5,
            "tension" : 0.0,
            "flatten" : 0.0
        },
        "angry" : {
            "openness" : 1.25,
            "turn" : 1.0,
            "squint" : 0.75,
            "dilation" : 0.25,
            "droopiness" : 0.75,
            "tension" : 0.0,
            "flatten" : 0.0
        },
        "pain" : {
            "openness" : 0.0,
            "turn" : 1.0,
            "squint" : 1.0,
            "dilation" : 0.0,
            "droopiness" : 0.0,
            "tension" : 1.0,
            "flatten" : 0.0
        },
        "sleepy" : {
            "openness" : 0.0,
            "turn" : 0.25,
            "squint" : 0.75,
            "dilation" : 0.1,
            "droopiness" : 0.5,
            "tension" : 0.0,
            "flatten" : 0.0
        },
        "scared" : {
            "openness" : -0.1,
            "turn" : 1.0,
            "squint" : 0.0,
            "dilation" : 1.0,
            "droopiness" : 0.5,
            "tension" : 0.0,
            "flatten" : 0.5
        },
        "happy" : {
            "openness" : 0.0,
            "turn" : 0.0,
            "squint" : 1.0,
            "dilation" : 0.25,
            "droopiness" : 0.5,
            "tension" : 0.0,
            "flatten" : 0.0
        },
        "excited" : {
            "openness" : 0.1,
            "turn" : 0.5,
            "squint" : 0.0,
            "dilation" : 1.0,
            "droopiness" : 0.5,
            "tension" : 0.0,
            "flatten" : 0.0
        },
    }
    def __init__(self):
        # Default pattern
        self.fill = "grey"
        self.nose = "black"
        self.white_neck = False
        self.brightness = 1.0
        self.spots = ["grey"]
        self.tabby = "grey"
        # Default mood (neutral)
        self.openness = 0.0
        self.turn = 0.0
        self.squint = 0.25
        self.dilation = 0.1
        self.droopiness = 0.5
        self.tension = 0.0
        self.flatten = 0.0
    def rescale_1d(self, a, im_size_tuple):
        return round(a*(im_size_tuple[0]+im_size_tuple[1])/(self.__ref_width+self.__ref_height))
    def rescale(self, x_y_tuple, im_size_tuple):
        return round(x_y_tuple[0]*im_size_tuple[0]/self.__ref_width), round(x_y_tuple[1]*im_size_tuple[1]/self.__ref_height)
    def draw_rectangle(self, im, xy, **kwargs):
        xy = [self.rescale(ab, im.size) for ab in xy]
        draw_obj = ImageDraw.Draw(im)
        draw_obj.rectangle(xy, **kwargs)
    def draw_ellipse(self, im, xy, **kwargs):
        xy = [self.rescale(ab, im.size) for ab in xy]
        draw_obj = ImageDraw.Draw(im)
        draw_obj.ellipse(xy, **kwargs)
    def draw_arc(self, im, xy, width, **kwargs):
        xy = [self.rescale(ab, im.size) for ab in xy]
        width = self.rescale_1d(width, im.size)
        draw_obj = ImageDraw.Draw(im)
        draw_obj.arc(xy=xy, width=width, **kwargs)
    def draw_pieslice(self, im, xy, **kwargs):
        xy = [self.rescale(ab, im.size) for ab in xy]
        draw_obj = ImageDraw.Draw(im)
        draw_obj.pieslice(xy, **kwargs)
    def draw_polygon(self, im, xy, **kwargs):
        xy = [self.rescale(ab, im.size) for ab in xy]
        draw_obj = ImageDraw.Draw(im)
        draw_obj.polygon(xy, **kwargs)
    def draw_line(self, im, xy, width, **kwargs):
        xy = [self.rescale(ab, im.size) for ab in xy]
        width = self.rescale_1d(width, im.size)
        draw_obj = ImageDraw.Draw(im)
        draw_obj.polygon(xy, **kwargs)
    # Define a disorted re-centered ellipse
    def distorted_ellipse(self, im, topleft_xy, bottomright_xy, center_xy, fill_rgb, quadrants=(True, True, True, True), stroke_width=(0, 0, 0, 0)):
        topleft_xy = self.rescale(topleft_xy, im.size)
        bottomright_xy = self.rescale(bottomright_xy, im.size)
        center_xy = self.rescale(center_xy, im.size)
        draw_obj = ImageDraw.Draw(im)
        stroke_width = [self.rescale_1d(a, im.size) for a in stroke_width]
        # Given a corner and a center, determine the opposiste corner
        # If you draw this on paper, the other corner is on the opposite side of the center
        # that the original corner is
        def opposite_corner(corner, center):
            return (2*center[0] - corner[0], 2*center[1] - corner[1])
        # Top left
        if quadrants[0]:
            draw_obj.pieslice(xy=[topleft_xy,
                                opposite_corner(topleft_xy, center_xy)],
                                start=180,
                                end=270,
                                fill=fill_rgb)
            if stroke_width[0]:
                draw_obj.arc(xy=[topleft_xy,
                                opposite_corner(topleft_xy, center_xy)],
                                start=180,
                                end=270,
                                fill="black",
                                width=stroke_width[0])
        # Top right
        if quadrants[1]:
            topright_xy = (bottomright_xy[0], topleft_xy[1])
            topright_xy_opp = opposite_corner(topright_xy, center_xy)
            draw_obj.pieslice(xy=[(topright_xy_opp[0], topright_xy[1]),
                                (topright_xy[0], topright_xy_opp[1])],
                                start=270,
                                end=0,
                                fill=fill_rgb)
            if stroke_width[1]:
                draw_obj.arc(xy=[(topright_xy_opp[0], topright_xy[1]),
                                (topright_xy[0], topright_xy_opp[1])],
                                start=270,
                                end=0,
                                fill="black",
                                width=stroke_width[1])
        # Bottom right
        if quadrants[2]:
            bottomright_xy_opp = opposite_corner(bottomright_xy, center_xy)
            draw_obj.pieslice(xy=[(bottomright_xy_opp[0], bottomright_xy_opp[1]),
                                (bottomright_xy[0], bottomright_xy[1])],
                                start=0,
                                end=90,
                                fill=fill_rgb)
            if stroke_width[2]:
                draw_obj.arc(xy=[(bottomright_xy_opp[0], bottomright_xy_opp[1]),
                                (bottomright_xy[0], bottomright_xy[1])],
                                start=0,
                                end=90,
                                fill="black",
                                width=stroke_width[2])
        # Bottom left
        if quadrants[3]:
            bottomleft_xy = (topleft_xy[0], bottomright_xy[1])
            bottomleft_xy_opp = opposite_corner(bottomleft_xy, center_xy)
            draw_obj.pieslice(xy=[(bottomleft_xy[0], bottomleft_xy_opp[1]),
                                (bottomleft_xy_opp[0], bottomleft_xy[1])],
                                start=90,
                                end=180,
                                fill=fill_rgb)
            if stroke_width[3]:
                draw_obj.arc(xy=[(bottomleft_xy[0], bottomleft_xy_opp[1]),
                                (bottomleft_xy_opp[0], bottomleft_xy[1])],
                                start=90,
                                end=180,
                                fill="black",
                                width=stroke_width[3])
    def set_pattern(self, pattern_name=None, fill=None, nose=None, white_neck=None, brightness=None, spots=None, tabby=None):
        if pattern_name is not None:
            for key in self.pattern_dict[pattern_name]:
                setattr(self, key, self.pattern_dict[pattern_name][key])
        if fill is not None:
            self.fill = fill
        if nose is not None:
            self.nose = nose
        if white_neck is not None:
            self.white_neck = white_neck
        if brightness is not None:
            self.brightness = brightness
        if spots is not None:
            self.spots = spots
        if tabby is not None:
            self.tabby = tabby
        return self
    def get_pattern(self, im):
        pattern = Image.new("RGBA", im.size, (255, 0, 0, 0))
        draw_obj = ImageDraw.Draw(pattern)
        if self.fill is not None:
            draw_obj.rectangle([(0, 0), (pattern.width, pattern.height)], fill=self.fill)
        if self.spots is not None:
            for i in range(12):
                x = (3 * i * pattern.width // 5) % pattern.width
                y = (5 * i * pattern.width // 7) % pattern.width
                s = (3*i*(pattern.width+pattern.height)//7) % ((pattern.width+pattern.height)//5)
                f = self.spots[i % len(self.spots)]
                draw_obj.ellipse([(x, y), (x+s, y+s)], f)
        elif self.tabby is not None:
            # M
            draw_obj.polygon([(12*pattern.width//32, 6*pattern.height//16),
                              (14*pattern.width//32, 4*pattern.height//16),
                              (15*pattern.width//32, 6*pattern.height//16),
                              (14*pattern.width//32, 5*pattern.height//16),
                              ], self.tabby)
            draw_obj.polygon([(16*pattern.width//32,  5*pattern.height//32),
                              (17*pattern.width//32,  9*pattern.height//32),
                              (16*pattern.width//32, 11*pattern.height//32),
                              (15*pattern.width//32,  9*pattern.height//32),
                              ], self.tabby)
            draw_obj.polygon([(20*pattern.width//32, 6*pattern.height//16),
                              (18*pattern.width//32, 4*pattern.height//16),
                              (17*pattern.width//32, 6*pattern.height//16),
                              (18*pattern.width//32, 5*pattern.height//16),
                              ], self.tabby)
            # Left markings
            draw_obj.polygon([( 3*pattern.width//32, 18*pattern.height//32),
                              ( 6*pattern.width//32, 15*pattern.height//32),
                              ( 9*pattern.width//32, 15*pattern.height//32),
                              ( 6*pattern.width//32, 16*pattern.height//32),
                              ], self.tabby)
            draw_obj.polygon([( 3*pattern.width//32, 20*pattern.height//32),
                              ( 6*pattern.width//32, 17*pattern.height//32),
                              ( 9*pattern.width//32, 17*pattern.height//32),
                              ( 6*pattern.width//32, 18*pattern.height//32),
                              ], self.tabby)
            draw_obj.polygon([( 6*pattern.width//32, 22*pattern.height//32),
                              ( 9*pattern.width//32, 19*pattern.height//32),
                              (12*pattern.width//32, 19*pattern.height//32),
                              ( 9*pattern.width//32, 20*pattern.height//32),
                              ], self.tabby)
            # Right markings
            draw_obj.polygon([( 29*pattern.width//32, 18*pattern.height//32),
                              ( 26*pattern.width//32, 15*pattern.height//32),
                              ( 23*pattern.width//32, 15*pattern.height//32),
                              ( 26*pattern.width//32, 16*pattern.height//32),
                              ], self.tabby)
            draw_obj.polygon([( 29*pattern.width//32, 20*pattern.height//32),
                              ( 26*pattern.width//32, 17*pattern.height//32),
                              ( 23*pattern.width//32, 17*pattern.height//32),
                              ( 26*pattern.width//32, 18*pattern.height//32),
                              ], self.tabby)
            draw_obj.polygon([( 26*pattern.width//32, 22*pattern.height//32),
                              ( 23*pattern.width//32, 19*pattern.height//32),
                              ( 20*pattern.width//32, 19*pattern.height//32),
                              ( 23*pattern.width//32, 20*pattern.height//32),
                              ], self.tabby)
        if self.white_neck:
            draw_obj.polygon([(pattern.width//2, pattern.height//2), (pattern.width, pattern.height), (0, pattern.height)], fill="white")
        if self.brightness != 1.0:
            enhance_obj = ImageEnhance.Brightness(pattern)
            pattern = enhance_obj.enhance(self.brightness)
        return pattern
    def set_mood(self, mood_name=None, openness = None, turn = None, squint = None, dilation = None, droopiness = None):
        if type(mood_name) is list:
            # Mix moods assuming they have equal weight
            # You can double a mood's weight by putting it in the list twice
            avg = dict()
            for k in self.mood_dict["neutral"]:
                avg[k] = sum(self.mood_dict[m][k] for m in mood_name)/len(mood_name)
            for key in avg:
                setattr(self, key, avg[key])
        elif type(mood_name) is dict:
            # Allows you to use a dictionary to mix moods with weights
            # Normalize data so that weights total to 1
            for m in mood_name:
                if mood_name[m] <= 0:
                    del mood_name[m]
            msum = sum(mood_name[k] for k in mood_name)
            if msum > 1:
                for k in mood_name:
                    mood_name[k] /= msum
            elif msum < 1:
                if "neutral" in mood_name:
                    for k in mood_name:
                        mood_name[k] /= msum
                else:
                    # If neutral not there, assume it makes up the rest
                    mood_name["neutral"] = 1-msum
            # Iterate through each mood key, calculating the weighted
            # mean of each
            avg = dict()
            for k in self.mood_dict["neutral"]:
                avg[k] = sum(self.mood_dict[m][k]*mood_name[m] for m in mood_name)
            for key in avg:
                setattr(self, key, avg[key])
        elif mood_name is not None:
            for key in self.mood_dict[mood_name]:
                setattr(self, key, self.mood_dict[mood_name][key])
        if openness is not None:
            self.openness = openness
        if turn is not None:
            self.turn = turn
        if squint is not None:
            self.squint = squint
        if dilation is not None:
            self.dilation = dilation
        if droopiness is not None:
            self.droopiness = droopiness
        return self

# Background
class Head(Cat):
    def __init__(self, width=1, height=1):
        super().__init__()
        self.w = width
        self.h = height
    def draw(self, im):
        # All of the classes' draw methods copy the given image
        # and return the modified copy. This means that you can
        # keep a history of your modifications, for example for
        # an animation of a sequence of images.
        im = im.copy()
        mask = Image.new("L", im.size, "white")
        ox = 1250
        oy = 1500
        self.draw_ellipse(mask, xy=[(ox-self.w*1000, oy-self.h*1000),
                         (ox+self.w*1000, oy+self.h*1000)],
                     fill="black")
        composite = Image.composite(im, self.get_pattern(im), mask)
        return composite

# A full background
class Block(Cat):
    def __init__(self):
        super().__init__()
    def draw(self, im):
        im = im.copy()
        im.paste(self.get_pattern(im))
        return im

# Mouth
class Mouth(Head):
    def __init__(self, 
                 chin_x_offset = 0.0, chin_y_offset = 0.0, 
                 width=1, height=1):
        super().__init__()
        self.chin_x_offset = chin_x_offset
        self.chin_y_offset = chin_y_offset
        self.w = width
        self.h = height
        self.brightness = 0.9
    def draw(self, im):
        uox = 1250
        uoy = 1950
        cox = 1250 * (1 + self.chin_x_offset)
        coy = 2150 * (1 + self.chin_y_offset + self.openness*0.1)
        im = im.copy()
        # Each part of the mouth is overlaid on the previous
        # lip over teeth, teeth over mouth hole
        # open mouth, basically a hole
        self.draw_rectangle(im, xy=[(uox-self.w*175, uoy-self.h*50),
                         (cox+self.w*175, coy)],
                     fill=(0, 0, 0))
        # upper teef
        upper_teefs = [
            (-150, 75, -100),
            (-100, 20,  -50),
            ( -50, 20,    0),
            (   0, 20,   50),
            (  50, 20,  100),
            ( 100, 75,  150),
            ]
        for t in upper_teefs:
            self.draw_ellipse(im, xy=[(uox+self.w*t[0], uoy-self.h*(50+t[1])),
                               (uox+self.w*t[2], uoy+self.h*(50+t[1]))],
                        fill=(255, 255, 255))
        # lower teef
        lower_teefs = [
            (-150, 75, -100),
            (-100, 20,  -50),
            ( -50, 20,    0),
            (   0, 20,   50),
            (  50, 20,  100),
            ( 100, 75,  150),
            ]
        for t in lower_teefs:
            self.draw_ellipse(im, xy=[(cox+self.w*t[0], coy-self.h*(175+t[1])),
                               (cox+self.w*t[2], coy)],
                        fill=(255, 255, 255))
        # upper lip
        self.draw_rectangle(im, xy=[(uox-self.w*175, uoy-self.h*50),
                         (uox+self.w*175, uoy+self.h*50)],
                     fill=(74, 44, 42))
        # lower lip
        self.draw_rectangle(im, xy=[(cox-self.w*175, coy-self.h*175),
                         (cox+self.w*175, coy)],
                     fill=(74, 44, 42))
        # chin
        mask = Image.new("L", im.size, "white")
        self.draw_ellipse(mask, xy=[(cox-self.w*200, coy-self.h*150),
                         (cox+self.w*200, coy+self.h*150)],
                     fill="black")
        composite = Image.composite(im, self.get_pattern(im), mask)
        return composite

# Left cheek
class LeftCheek(Head):
    def __init__(self, width=1, height=1):
        super().__init__()
        self.width = width
        self.height = height
        self.brightness = 0.95
    def draw(self, im):
        w = self.width*(1+self.tension/4)
        h = self.height
        im = im.copy()
        mask = Image.new("L", im.size, "white")
        ox = 1250
        oy = 1900
        self.distorted_ellipse(mask,
                          (ox-w*500, oy-h*200),
                          (ox, oy+h*200),
                          (ox-w*300, oy),
                          "black",
                          stroke_width=[0, 0, 15, 15])
        composite = Image.composite(im, self.get_pattern(im), mask)
        return composite

# Right cheek
class RightCheek(Head):
    def __init__(self, width=1, height=1):
        super().__init__()
        self.width = width
        self.height = height
        self.brightness = 0.95
    def draw(self, im):
        w = self.width*(1+self.tension/3)
        h = self.height
        im = im.copy()
        mask = Image.new("L", im.size, "white")
        ox = 1250
        oy = 1900
        self.distorted_ellipse(mask,
                          (ox, oy-h*200),
                          (ox+w*500, oy+h*200),
                          (ox+w*300, oy),
                          "black",
                          stroke_width=[0, 0, 15, 15])
        composite = Image.composite(im, self.get_pattern(im), mask)
        return composite

# Left ear
class LeftEar(Head):
    def __init__(self, width=1, height=1):
        super().__init__()
        self.w = width
        self.height = height
    def draw(self, im):
        h = (1 - self.flatten/2) * self.height
        t = self.turn
        mask = Image.new("L", im.size, "white")
        # Draw the outer ear first
        o_ox = 450
        o_oy = 800
        self.distorted_ellipse(mask,
                          (o_ox-self.w*200-t*100, o_oy-h*700+t*200),
                          (o_ox+self.w*600, o_oy+h*400),
                          (o_ox-t*100, o_oy+t*200),
                          "black")
        # Rescale rotation origin as well
        mask = mask.rotate(t*45, fillcolor="white",
                           center=self.rescale((o_ox, o_oy), mask.size))
        composite = Image.composite(im, self.get_pattern(im), mask)
        # Now the inner ear, same idea, but different
        # Darken the inner ear
        inner_ear = self.get_pattern(im)
        enchance_obj = ImageEnhance.Brightness(inner_ear)
        inner_ear = enchance_obj.enhance(0.9)
        inner_ear_mask = Image.new("L", im.size, "white")
        i_ox = 450
        i_oy = 600
        self.distorted_ellipse(inner_ear_mask,
                          (i_ox-(t+self.w)*100, i_oy-h*400+t*200),
                          (i_ox+(1-t)*self.w*300, i_oy+h*200+t*100),
                          (i_ox-t*150, i_oy),
                          "black")
        # Rescale rotation origin as well
        inner_ear_mask = inner_ear_mask.rotate(t*45, fillcolor="white",
                         center=self.rescale((o_ox, o_oy), mask.size))
        # Perform the second composite
        composite = Image.composite(composite, inner_ear, inner_ear_mask)
        return composite

# Right ear
class RightEar(Head):
    def __init__(self, width=1, height=1):
        super().__init__()
        self.w = width
        self.height = height
    def draw(self, im):
        h = (1 - self.flatten/2) * self.height
        t = self.turn
        mask = Image.new("L", im.size, "white")
        # Draw the outer ear first
        o_ox = 2050
        o_oy = 800
        self.distorted_ellipse(mask,
                          (o_ox-self.w*600, o_oy-h*700+t*200),
                          (o_ox+self.w*200+t*100, o_oy+h*400),
                          (o_ox+t*100, o_oy+t*200),
                          "black")
        # Rescale rotation origin as well
        mask = mask.rotate(t*-45, fillcolor="white",
                           center=self.rescale((o_ox, o_oy), mask.size))
        composite = Image.composite(im, self.get_pattern(im), mask)
        # Now the inner ear, same idea, but different
        # Darken the inner ear
        inner_ear = self.get_pattern(im)
        enchance_obj = ImageEnhance.Brightness(inner_ear)
        inner_ear = enchance_obj.enhance(0.9)
        inner_ear_mask = Image.new("L", im.size, "white")
        i_ox = 2050
        i_oy = 600
        self.distorted_ellipse(inner_ear_mask,
                          (i_ox-(1-t)*self.w*300, i_oy-h*400+t*200),
                          (i_ox+(t+self.w)*100, i_oy+h*200+t*100),
                          (i_ox+t*150, i_oy),
                          "black")
        # Rescale rotation origin as well
        inner_ear_mask = inner_ear_mask.rotate(t*-45, fillcolor="white",
                         center=self.rescale((o_ox, o_oy), mask.size))
        # Perform the second composite
        composite = Image.composite(composite, inner_ear, inner_ear_mask)
        return composite

# Nose
class Nose(Head):
    def __init__(self, width=1, height=1, upper_lip=True):
        super().__init__()
        self.w = width
        self.h = height
        self.upper_lip = upper_lip
    def draw(self, im):
        im = im.copy()
        ox = 1250
        oy = 1700
        if self.upper_lip:
            self.draw_line(im, xy=[(ox, oy+self.h*100), (ox, oy+self.h*200)], fill=(0, 0, 0), width=15)
        self.draw_polygon(im, xy=[(ox-self.w*200, oy-self.h*100),
                                  (ox, oy+self.h*100),
                                  (ox+self.w*200, oy-self.h*100)],
                                  fill=self.nose)
        return im

# Left eye
class LeftEye(Head):
    def __init__(self,
                 eye_width=1, eye_height=1,
                 pupil_width=1, pupil_height=1,
                 eye_fill=(9, 121, 105)):
        super().__init__()
        self.eye_width = eye_width
        self.eye_height = eye_height
        self.pupil_width = pupil_width
        self.pupil_height = pupil_height
        self.eye_fill = eye_fill
    def draw(self, im):
        ew = self.eye_width
        eh = self.eye_height * (1.0-self.squint)
        pw = self.pupil_width * (0.7+3*self.dilation)
        ph = self.pupil_height * (0.9+0.5*self.dilation)
        ef = self.eye_fill
        eox = 850
        eoy = 1200
        pox = 850
        poy = 1200
        # Eyes with mask
        # Use the mask to set the boundaries of the pupil (black part of eye)
        # With a mask, the pupil can get really big without escaping the eyes
        # The cat can also squint if it wants to
        mask = Image.new("L", im.size, "white")
        # Left eye mask
        self.draw_pieslice(mask,
                          [(eox-ew*250, eoy-eh*200),
                          (eox+ew*250, eoy+eh*200)],
                          start=180, end=0,
                          fill="black")
        self.distorted_ellipse(mask,
                          (eox-ew*250, eoy-eh*200),
                          (eox+ew*250, eoy+eh*200),
                          (eox-50, eoy),
                          "black",
                          quadrants=(False, False, True, True))
        eye = Image.new("RGBA", im.size, ef)
        # Rescale rotation origin as well
        mask = mask.rotate(-30, fillcolor="white",
                         center=self.rescale((eox, eoy), mask.size))
        # Pupil
        self.draw_ellipse(eye, xy=[(pox-pw*50, poy-ph*150),
                             (pox+pw*50, poy+ph*150)],
                             fill=(0, 0, 0))
        # Perform the composite
        composite = Image.composite(im, eye, mask)
        return composite

# Right eye
class RightEye(Head):
    def __init__(self,
                 eye_width=1, eye_height=1,
                 pupil_width=1, pupil_height=1,
                 eye_fill=(9, 121, 105)):
        super().__init__()
        self.eye_width = eye_width
        self.eye_height = eye_height
        self.pupil_width = pupil_width
        self.pupil_height = pupil_height
        self.eye_fill = eye_fill
    def draw(self, im):
        ew = self.eye_width
        eh = self.eye_height * (1.0-self.squint)
        pw = self.pupil_width * (0.7+3*self.dilation)
        ph = self.pupil_height * (0.9+0.5*self.dilation)
        ef = self.eye_fill
        eox = 1650
        eoy = 1200
        pox = 1650
        poy = 1200
        # Eyes with mask
        # Use the mask to set the boundaries of the pupil (black part of eye)
        # With a mask, the pupil can get really big without escaping the eyes
        # The cat can also squint if it wants to
        mask = Image.new("L", im.size, "white")
        # Left eye mask
        self.distorted_ellipse(mask,
                          (eox-ew*250, eoy-eh*200),
                          (eox+ew*250, eoy+eh*200),
                          (eox-50, eoy),
                          "black",
                          quadrants=(True, True, False, False))
        self.distorted_ellipse(mask,
                          (eox-ew*250, eoy-eh*200),
                          (eox+ew*250, eoy+eh*200),
                          (eox+50, eoy),
                          "black",
                          quadrants=(False, False, True, True))
        eye = Image.new("RGBA", im.size, ef)
        # Rescale rotation origin as well
        mask = mask.rotate(30, fillcolor="white",
                         center=self.rescale((eox, eoy), mask.size))
        # Pupil
        self.draw_ellipse(eye, xy=[(pox-pw*50, poy-ph*150),
                             (pox+pw*50, poy+ph*150)],
                             fill=(0, 0, 0))
        # Perform the composite
        composite = Image.composite(im, eye, mask)
        return composite

# Left whisker
# Whiskers are portions of a circle's circumference
# Are the whiskers move/droop, the circle moves along another
# hidden circle, while the arc similarly slides (start and end angles)
# What this all does is create a curve that spins on an origin
class LeftWhisker(Head):
    def __init__(self, width=1, height=1,
                 length=0.75,
                 fill="white", thickness=2,
                 whiskers = 5):
        super().__init__()
        self.w = width
        self.h = height
        self.f = fill
        self.l = length
        self.t = thickness
        self.ox = 1000
        self.oy = 1850
        self.flip = False
        self.n = whiskers
    def draw(self, im):
        im = im.copy()
        for w in range(self.n):
            oy = self.oy + w//2*50
            d = self.droopiness+w/5
            if self.flip:
                ox = self.ox + w%2*100
                phase = d*math.pi/2
                s=180+d*90
                e=300+d*90*self.l
            else:
                ox = self.ox - w%2*100
                phase = (2-d)*math.pi/2
                s=240-d*90*self.l
                e=0-d*90
            self.draw_arc(im,
                        xy = [
                            (ox+400*self.w*(math.cos(phase)-1),
                            oy+400*self.h*(math.sin(phase)-1)),
                            (ox+400*self.w*(math.cos(phase)+1),
                            oy+400*self.h*(math.sin(phase)+1))  
                        ],
                        start=s,
                        end=e,
                        fill=self.f,
                        width=self.t)
        return im

class RightWhisker(LeftWhisker):
    def __init__(self, width=1, height=1,
                 length=0.75,
                 fill="white", thickness=2,
                 whiskers=5):
        super().__init__()
        self.w = width
        self.h = height
        self.f = fill
        self.d = self.droopiness
        self.l = length
        self.t = thickness
        self.ox = 1500
        self.oy = 1850
        self.flip = True
        self.n = whiskers

class LeftEyebrow(LeftWhisker):
    def __init__(self, width=1, height=1,
                 length=0.75,
                 fill="white", thickness=1,
                 whiskers=2):
        super().__init__()
        self.w = width
        self.h = height
        self.f = fill
        self.d = self.droopiness
        self.l = length
        self.t = thickness
        self.ox = 1050
        self.oy = 900
        self.flip = False
        self.n = whiskers

class RightEyebrow(LeftWhisker):
    def __init__(self, width=1, height=1,
                 length=0.75,
                 fill="white", thickness=1,
                 whiskers=2):
        super().__init__()
        self.w = width
        self.h = height
        self.f = fill
        self.d = self.droopiness
        self.l = length
        self.t = thickness
        self.ox = 1450
        self.oy = 900
        self.flip = True
        self.n = whiskers
