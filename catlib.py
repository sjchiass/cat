import math
import random
from PIL import Image, ImageDraw, ImageEnhance

# Background
class Head:
    # The canvas size the layers were designed in.
    # The actual output images are rescaled from this design size
    # to the actual size of the image being drawn.
    __ref_width = 2500
    __ref_height = 2500
    pattern_dict = {
        "orange" : {"fill" : (205, 127, 50),
                    "nose" : (160, 82, 45),
                    "white_neck" : False},
        "orange tabby" : {"fill" : (205, 127, 50),
                    "nose" : (255, 167, 166),
                    "white_neck" : True},
        "tuxedo" : {"fill" : (32, 32, 36),
                          "nose" : "black",
                    "white_neck" : True},
        "black" : {"fill" : (32, 32, 36),
                          "nose" : "black",
                    "white_neck" : False},
        "grey tabby" : {"fill" : "grey",
                    "nose" : (160, 82, 45),
                    "white_neck" : True},
        "russian blue" : {"fill" : (102, 109, 113),
                          "nose" : (25, 30, 32),
                    "white_neck" : False},
        "calico" : {"fill" : (32, 32, 36),
                    "nose" : (160, 82, 45),
                    "white_neck" : True,
                    "spots" : [(205, 127, 50), (160, 73, 30)]},
        "calico_spots" : {"fill" : "white",
                    "nose" : (255, 167, 166),
                    "white_neck" : False,
                    "spots" : [(205, 127, 50), (160, 73, 30), (32, 32, 36)]},
        "tortoiseshell" : {"fill" : (32, 32, 36),
                    "nose" : "black",
                    "white_neck" : False,
                    "spots" : [(205, 127, 50), (160, 73, 30)]}
    }
    def __init__(self, width=1, height=1):
        self.w = width
        self.h = height
        self.fill = None
        self.nose = None
        self.white_neck = False
        self.brightness = 1.0
        self.spots = None
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
    def set_pattern(self, pattern_name=None, fill=None, nose=None, white_neck=None, brightness=None, spots=None):
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
        return self
    def get_pattern(self, im):
        pattern = Image.new("RGB", im.size, (255, 255, 255))
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
        if self.white_neck:
            draw_obj.polygon([(pattern.width/2, pattern.height/2), (pattern.width, pattern.height), (0, pattern.height)], fill="white")
        if self.brightness != 1.0:
            enhance_obj = ImageEnhance.Brightness(pattern)
            pattern = enhance_obj.enhance(self.brightness)
        return pattern

# Mouth
class Mouth(Head):
    def __init__(self, 
                 openness = 0.0, 
                 chin_x_offset = 0.0, chin_y_offset = 0.0, 
                 width=1, height=1):
        self.uox = 1250
        self.uoy = 1950
        self.cox = 1250 * (1 + chin_x_offset)
        self.coy = 2150 * (1 + chin_y_offset + openness*0.1)
        self.w = width
        self.h = height
        self.fill = None
        self.nose = None
        self.white_neck = False
        self.brightness = 0.9
        self.spots = None
    def draw(self, im):
        im = im.copy()
        # Each part of the mouth is overlaid on the previous
        # lip over teeth, teeth over mouth hole
        # open mouth, basically a hole
        self.draw_rectangle(im, xy=[(self.uox-self.w*175, self.uoy-self.h*50),
                         (self.cox+self.w*175, self.coy)],
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
            self.draw_ellipse(im, xy=[(self.uox+self.w*t[0], self.uoy-self.h*(50+t[1])),
                               (self.uox+self.w*t[2], self.uoy+self.h*(50+t[1]))],
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
            self.draw_ellipse(im, xy=[(self.cox+self.w*t[0], self.coy-self.h*(175+t[1])),
                               (self.cox+self.w*t[2], self.coy)],
                        fill=(255, 255, 255))
        # upper lip
        self.draw_rectangle(im, xy=[(self.uox-self.w*175, self.uoy-self.h*50),
                         (self.uox+self.w*175, self.uoy+self.h*50)],
                     fill=(74, 44, 42))
        # lower lip
        self.draw_rectangle(im, xy=[(self.cox-self.w*175, self.coy-self.h*175),
                         (self.cox+self.w*175, self.coy)],
                     fill=(74, 44, 42))
        # chin
        mask = Image.new("L", im.size, "white")
        self.draw_ellipse(mask, xy=[(self.cox-self.w*200, self.coy-self.h*150),
                         (self.cox+self.w*200, self.coy+self.h*150)],
                     fill="black")
        composite = Image.composite(im, self.get_pattern(im), mask)
        return composite

# Left cheek
class LeftCheek(Head):
    def __init__(self, width=1, height=1):
        self.w = width
        self.h = height
        self.fill = None
        self.nose = None
        self.white_neck = False
        self.brightness = 0.95
        self.spots = None
    def draw(self, im):
        im = im.copy()
        mask = Image.new("L", im.size, "white")
        ox = 1250
        oy = 1900
        self.distorted_ellipse(mask,
                          (ox-self.w*500, oy-self.h*200),
                          (ox, oy+self.h*200),
                          (ox-self.w*300, oy),
                          "black",
                          stroke_width=[0, 0, 15, 15])
        composite = Image.composite(im, self.get_pattern(im), mask)
        return composite

# Right cheek
class RightCheek(Head):
    def __init__(self, width=1, height=1):
        self.w = width
        self.h = height
        self.fill = None
        self.nose = None
        self.white_neck = False
        self.brightness = 0.95
        self.spots = None
    def draw(self, im):
        im = im.copy()
        mask = Image.new("L", im.size, "white")
        ox = 1250
        oy = 1900
        self.distorted_ellipse(mask,
                          (ox, oy-self.h*200),
                          (ox+self.w*500, oy+self.h*200),
                          (ox+self.w*300, oy),
                          "black",
                          stroke_width=[0, 0, 15, 15])
        composite = Image.composite(im, self.get_pattern(im), mask)
        return composite

# Left ear
class LeftEar(Head):
    def __init__(self, width=1, height=1,
                 turn=0.0):
        self.w = width
        self.h = height
        self.t = turn
        self.fill = None
        self.nose = None
        self.white_neck = False
        self.brightness = 1.0
        self.spots = None
    def draw(self, im):
        mask = Image.new("L", im.size, "white")
        # Draw the outer ear first
        o_ox = 450
        o_oy = 800
        self.distorted_ellipse(mask,
                          (o_ox-self.w*200-self.t*100, o_oy-self.h*700+self.t*200),
                          (o_ox+self.w*600, o_oy+self.h*400),
                          (o_ox-self.t*100, o_oy+self.t*200),
                          "black")
        # Rescale rotation origin as well
        mask = mask.rotate(self.t*45, fillcolor="white",
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
                          (i_ox-(self.t+self.w)*100, i_oy-self.h*400+self.t*200),
                          (i_ox+(1-self.t)*self.w*300, i_oy+self.h*200+self.t*100),
                          (i_ox-self.t*150, i_oy),
                          "black")
        # Rescale rotation origin as well
        inner_ear_mask = inner_ear_mask.rotate(self.t*45, fillcolor="white",
                         center=self.rescale((o_ox, o_oy), mask.size))
        # Perform the second composite
        composite = Image.composite(composite, inner_ear, inner_ear_mask)
        return composite

# Right ear
class RightEar(Head):
    def __init__(self, width=1, height=1,
                 turn=0.0):
        self.w = width
        self.h = height
        self.t = turn
        self.fill = None
        self.nose = None
        self.white_neck = False
        self.brightness = 1.0
        self.spots = None
    def draw(self, im):
        mask = Image.new("L", im.size, "white")
        # Draw the outer ear first
        o_ox = 2050
        o_oy = 800
        self.distorted_ellipse(mask,
                          (o_ox-self.w*600, o_oy-self.h*700+self.t*200),
                          (o_ox+self.w*200+self.t*100, o_oy+self.h*400),
                          (o_ox+self.t*100, o_oy+self.t*200),
                          "black")
        # Rescale rotation origin as well
        mask = mask.rotate(self.t*-45, fillcolor="white",
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
                          (i_ox-(1-self.t)*self.w*300, i_oy-self.h*400+self.t*200),
                          (i_ox+(self.t+self.w)*100, i_oy+self.h*200+self.t*100),
                          (i_ox+self.t*150, i_oy),
                          "black")
        # Rescale rotation origin as well
        inner_ear_mask = inner_ear_mask.rotate(self.t*-45, fillcolor="white",
                         center=self.rescale((o_ox, o_oy), mask.size))
        # Perform the second composite
        composite = Image.composite(composite, inner_ear, inner_ear_mask)
        return composite

# Nose
class Nose(Head):
    def __init__(self, width=1, height=1, upper_lip=True):
        self.w = width
        self.h = height
        self.upper_lip = upper_lip
        self.fill = None
        self.nose = (160, 82, 45)
        self.white_neck = False
        self.brightness = 1.0
        self.spots = None
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
                 squint = 0.25,
                 dilation = 0.1,
                 eye_width=1, eye_height=1,
                 pupil_width=1, pupil_height=1,
                 eye_fill=(9, 121, 105)):
        self.ew = eye_width
        self.eh = eye_height * (1.25-squint)
        self.pw = pupil_width * (0.7+3*dilation)
        self.ph = pupil_height * (0.9+0.5*dilation)
        self.ef = eye_fill
    def draw(self, im):
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
                          [(eox-self.ew*250, eoy-self.eh*200),
                          (eox+self.ew*250, eoy+self.eh*200)],
                          start=180, end=0,
                          fill="black")
        self.distorted_ellipse(mask,
                          (eox-self.ew*250, eoy-self.eh*200),
                          (eox+self.ew*250, eoy+self.eh*200),
                          (eox-50, eoy),
                          "black",
                          quadrants=(False, False, True, True))
        eye = Image.new("RGBA", im.size, self.ef)
        # Rescale rotation origin as well
        mask = mask.rotate(-30, fillcolor="white",
                         center=self.rescale((eox, eoy), mask.size))
        # Pupil
        self.draw_ellipse(eye, xy=[(pox-self.pw*50, poy-self.ph*150),
                             (pox+self.pw*50, poy+self.ph*150)],
                             fill=(0, 0, 0))
        # Perform the composite
        composite = Image.composite(im, eye, mask)
        return composite

# Right eye
class RightEye(Head):
    def __init__(self,
                 squint = 0.25,
                 dilation = 0.1,
                 eye_width=1, eye_height=1,
                 pupil_width=1, pupil_height=1,
                 eye_fill=(9, 121, 105)):
        self.ew = eye_width
        self.eh = eye_height * (1.25-squint)
        self.pw = pupil_width * (0.7+3*dilation)
        self.ph = pupil_height * (0.9+0.5*dilation)
        self.ef = eye_fill
    def draw(self, im):
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
                          (eox-self.ew*250, eoy-self.eh*200),
                          (eox+self.ew*250, eoy+self.eh*200),
                          (eox-50, eoy),
                          "black",
                          quadrants=(True, True, False, False))
        self.distorted_ellipse(mask,
                          (eox-self.ew*250, eoy-self.eh*200),
                          (eox+self.ew*250, eoy+self.eh*200),
                          (eox+50, eoy),
                          "black",
                          quadrants=(False, False, True, True))
        eye = Image.new("RGBA", im.size, self.ef)
        # Rescale rotation origin as well
        mask = mask.rotate(30, fillcolor="white",
                         center=self.rescale((eox, eoy), mask.size))
        # Pupil
        self.draw_ellipse(eye, xy=[(pox-self.pw*50, poy-self.ph*150),
                             (pox+self.pw*50, poy+self.ph*150)],
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
                 droopiness=0.5, length=0.75,
                 fill="white", thickness=2,
                 whiskers = 5):
        self.w = width
        self.h = height
        self.f = fill
        self.d = droopiness
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
            d = self.d+w/5
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
                 droopiness=0.5, length=0.75,
                 fill="white", thickness=2,
                 whiskers=5):
        self.w = width
        self.h = height
        self.f = fill
        self.d = droopiness
        self.l = length
        self.t = thickness
        self.ox = 1500
        self.oy = 1850
        self.flip = True
        self.n = whiskers

class LeftEyebrow(LeftWhisker):
    def __init__(self, width=1, height=1,
                 droopiness=0.0, length=0.75,
                 fill="white", thickness=1,
                 whiskers=2):
        self.w = width
        self.h = height
        self.f = fill
        self.d = droopiness
        self.l = length
        self.t = thickness
        self.ox = 1050
        self.oy = 900
        self.flip = False
        self.n = whiskers

class RightEyebrow(LeftWhisker):
    def __init__(self, width=1, height=1,
                 droopiness=0.0, length=0.75,
                 fill="white", thickness=1,
                 whiskers=2):
        self.w = width
        self.h = height
        self.f = fill
        self.d = droopiness
        self.l = length
        self.t = thickness
        self.ox = 1450
        self.oy = 900
        self.flip = True
        self.n = whiskers
