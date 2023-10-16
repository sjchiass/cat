from PIL import Image, ImageDraw

# Define a disorted re-centered ellipse
def distorted_ellipse(draw_obj, topleft_xy, bottomright_xy, center_xy, fill_rgb, quadrants=(True, True, True, True), stroke_width=(0, 0, 0, 0)):
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

# Background
class Head:
    def __init__(self, width=1, height=1, fill=(205, 127, 50)):
        self.w = width
        self.h = height
        self.f = fill
    def draw(self, im):
        # All of the classes' draw methods copy the given image
        # and return the modified copy. This means that you can
        # keep a history of your modifications, for example for
        # an animation of a sequence of images.
        im = im.copy()
        draw = ImageDraw.Draw(im)
        ox = 1250
        oy = 1500
        draw.ellipse(xy=[(ox-self.w*1000, oy-self.h*1000),
                         (ox+self.w*1000, oy+self.h*1000)],
                     fill=self.f)
        return im

# Chin
class Mouth:
    def __init__(self, width=1, height=1, fill=(227, 150, 62)):
        self.w = width
        self.h = height
        self.f = fill
    def draw(self, im):
        im = im.copy()
        draw = ImageDraw.Draw(im)
        ox = 1250
        oy = 2150
        draw.ellipse(xy=[(ox-self.w*200, oy-self.h*150),
                         (ox+self.w*200, oy+self.h*150)],
                     fill=self.f)
        return im

# Left cheek
class LeftCheek:
    def __init__(self, width=1, height=1, fill=(242, 140, 40)):
        self.w = width
        self.h = height
        self.f = fill
    def draw(self, im):
        im = im.copy()
        draw = ImageDraw.Draw(im)
        ox = 1250
        oy = 1900
        distorted_ellipse(draw,
                          (ox-self.w*500, oy-self.h*200),
                          (ox, oy+self.h*200),
                          (ox-self.w*300, oy),
                          self.f,
                          stroke_width=[0, 0, 15, 15])
        return im

# Right cheek
class RightCheek:
    def __init__(self, width=1, height=1, fill=(242, 140, 40)):
        self.w = width
        self.h = height
        self.f = fill
    def draw(self, im):
        im = im.copy()
        draw = ImageDraw.Draw(im)
        ox = 1250
        oy = 1900
        distorted_ellipse(draw,
                          (ox, oy-self.h*200),
                          (ox+self.w*500, oy+self.h*200),
                          (ox+self.w*300, oy),
                          self.f,
                          stroke_width=[0, 0, 15, 15])
        return im

# Left ear
class LeftEar:
    def __init__(self, width=1, height=1,
                 turn=0.0,
                 inner_fill=(184, 115, 51),
                 outer_fill=(205, 127, 50)):
        self.w = width
        self.h = height
        self.t = turn
        self.i_f = inner_fill
        self.o_f = outer_fill
    def draw(self, im):
        mask = Image.new("L", im.size, "white")
        draw_mask = ImageDraw.Draw(mask)
        # Draw the outer ear first
        o_ox = 450
        o_oy = 800
        distorted_ellipse(draw_mask,
                          (o_ox-self.w*200-self.t*100, o_oy-self.h*700+self.t*200),
                          (o_ox+self.w*600, o_oy+self.h*400),
                          (o_ox-self.t*100, o_oy+self.t*200),
                          "black")
        mask = mask.rotate(self.t*45, fillcolor="white", center=(o_ox, o_oy))
        ear = Image.new("RGBA", im.size, self.o_f)
        draw_ear = ImageDraw.Draw(ear)
        i_ox = 450
        i_oy = 600
        distorted_ellipse(draw_ear,
                          (i_ox-(self.t+self.w)*100, i_oy-self.h*400+self.t*200),
                          (i_ox+(1-self.t)*self.w*300, i_oy+self.h*200+self.t*100),
                          (i_ox-self.t*150, i_oy),
                          self.i_f)
        ear = ear.rotate(self.t*45, fillcolor="white", center=(o_ox, o_oy))
        # Perform the composite
        composite = Image.composite(im, ear, mask)
        return composite

# Right ear
class RightEar:
    def __init__(self, width=1, height=1,
                 turn=0.0,
                 inner_fill=(184, 115, 51),
                 outer_fill=(205, 127, 50)):
        self.w = width
        self.h = height
        self.t = turn
        self.i_f = inner_fill
        self.o_f = outer_fill
    def draw(self, im):
    
        mask = Image.new("L", im.size, "white")
        draw_mask = ImageDraw.Draw(mask)
        # Draw the outer ear first
        o_ox = 2050
        o_oy = 800
        distorted_ellipse(draw_mask,
                          (o_ox-self.w*600, o_oy-self.h*700+self.t*200),
                          (o_ox+self.w*200+self.t*100, o_oy+self.h*400),
                          (o_ox+self.t*100, o_oy+self.t*200),
                          "black")
        mask = mask.rotate(self.t*-45, fillcolor="white", center=(o_ox, o_oy))
        ear = Image.new("RGBA", im.size, self.o_f)
        draw_ear = ImageDraw.Draw(ear)
        i_ox = 2050
        i_oy = 600
        distorted_ellipse(draw_ear,
                          (i_ox-(1-self.t)*self.w*300, i_oy-self.h*400+self.t*200),
                          (i_ox+(self.t+self.w)*100, i_oy+self.h*200+self.t*100),
                          (i_ox+self.t*150, i_oy),
                          self.i_f)
        ear = ear.rotate(self.t*-45, fillcolor="white", center=(o_ox, o_oy))
        # Perform the composite
        composite = Image.composite(im, ear, mask)
        return composite

# Nose
class Nose:
    def __init__(self, width=1, height=1, upper_lip=True, fill=(160, 82, 45)):
        self.w = width
        self.h = height
        self.upper_lip = upper_lip
        self.f = fill
    def draw(self, im):
        im = im.copy()
        draw = ImageDraw.Draw(im)
        ox = 1250
        oy = 1700
        if self.upper_lip:
            draw.line(xy=[(ox, oy+self.h*100), (ox, oy+self.h*200)], fill=(0, 0, 0), width=15)
        draw.polygon(xy=[(ox-self.w*200, oy-self.h*100),
                                  (ox, oy+self.h*100),
                                  (ox+self.w*200, oy-self.h*100)],
                                  fill=self.f)
        return im

# Left eye
class LeftEye:
    def __init__(self, eye_width=1, eye_height=1,
                 pupil_width=1, pupil_height=1,
                 eye_fill=(9, 121, 105)):
        self.ew = eye_width
        self.eh = eye_height
        self.pw = pupil_width
        self.ph = pupil_height
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
        draw_mask = ImageDraw.Draw(mask)
        # Left eye mask
        distorted_ellipse(draw_mask,
                          (eox-self.ew*250, eoy-self.eh*200),
                          (eox+self.ew*250, eoy+self.eh*200),
                          (eox+50, eoy),
                          "black",
                          quadrants=(True, True, False, False))
        distorted_ellipse(draw_mask,
                          (eox-self.ew*250, eoy-self.eh*200),
                          (eox+self.ew*250, eoy+self.eh*200),
                          (eox-50, eoy),
                          "black",
                          quadrants=(False, False, True, True))
        mask = mask.rotate(-30, fillcolor="white", center=(eox, eoy))
        eye = Image.new("RGBA", im.size, self.ef)
        draw_eye = ImageDraw.Draw(eye)
        # Pupil
        draw_eye.ellipse(xy=[(pox-self.pw*50, poy-self.ph*150),
                             (pox+self.pw*50, poy+self.ph*150)],
                             fill=(0, 0, 0))
        # Perform the composite
        composite = Image.composite(im, eye, mask)
        return composite

# Right eye
class RightEye:
    def __init__(self, eye_width=1, eye_height=1,
                 pupil_width=1, pupil_height=1,
                 eye_fill=(9, 121, 105)):
        self.ew = eye_width
        self.eh = eye_height
        self.pw = pupil_width
        self.ph = pupil_height
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
        draw_mask = ImageDraw.Draw(mask)
        # Left eye mask
        distorted_ellipse(draw_mask,
                          (eox-self.ew*250, eoy-self.eh*200),
                          (eox+self.ew*250, eoy+self.eh*200),
                          (eox-50, eoy),
                          "black",
                          quadrants=(True, True, False, False))
        distorted_ellipse(draw_mask,
                          (eox-self.ew*250, eoy-self.eh*200),
                          (eox+self.ew*250, eoy+self.eh*200),
                          (eox+50, eoy),
                          "black",
                          quadrants=(False, False, True, True))
        mask = mask.rotate(30, fillcolor="white", center=(eox, eoy))
        eye = Image.new("RGBA", im.size, self.ef)
        draw_eye = ImageDraw.Draw(eye)
        # Pupil
        draw_eye.ellipse(xy=[(pox-self.pw*50, poy-self.ph*150),
                             (pox+self.pw*50, poy+self.ph*150)],
                             fill=(0, 0, 0))
        # Perform the composite
        composite = Image.composite(im, eye, mask)
        return composite