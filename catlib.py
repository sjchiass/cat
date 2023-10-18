from PIL import Image, ImageDraw

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
    @staticmethod
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

# Mouth
class Mouth(Head):
    def __init__(self, 
                 openness = 0.0, 
                 chin_x_offset = 0.0, chin_y_offset = 0.0, 
                 width=1, height=1,
                 fill=(227, 150, 62)):
        self.uox = 1250
        self.uoy = 1950
        self.cox = 1250 * (1 + chin_x_offset)
        self.coy = 2150 * (1 + chin_y_offset + openness*0.1)
        self.w = width
        self.h = height
        self.f = fill
    def draw(self, im):
        im = im.copy()
        draw = ImageDraw.Draw(im)
        # Each part of the mouth is overlaid on the previous
        # lip over teeth, teeth over mouth hole
        # open mouth, basically a hole
        draw.rectangle(xy=[(self.uox-self.w*175, self.uoy-self.h*50),
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
            draw.ellipse(xy=[(self.uox+self.w*t[0], self.uoy-self.h*(50+t[1])),
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
            draw.ellipse(xy=[(self.cox+self.w*t[0], self.coy-self.h*(175+t[1])),
                               (self.cox+self.w*t[2], self.coy)],
                        fill=(255, 255, 255))
        # upper lip
        draw.rectangle(xy=[(self.uox-self.w*175, self.uoy-self.h*50),
                         (self.uox+self.w*175, self.uoy+self.h*50)],
                     fill=(74, 44, 42))
        # lower lip
        draw.rectangle(xy=[(self.cox-self.w*175, self.coy-self.h*175),
                         (self.cox+self.w*175, self.coy)],
                     fill=(74, 44, 42))
        # chin
        draw.ellipse(xy=[(self.cox-self.w*200, self.coy-self.h*150),
                         (self.cox+self.w*200, self.coy+self.h*150)],
                     fill=self.f)
        return im

# Left cheek
class LeftCheek(Head):
    def __init__(self, width=1, height=1, fill=(242, 140, 40)):
        self.w = width
        self.h = height
        self.f = fill
    def draw(self, im):
        im = im.copy()
        draw = ImageDraw.Draw(im)
        ox = 1250
        oy = 1900
        self.distorted_ellipse(draw,
                          (ox-self.w*500, oy-self.h*200),
                          (ox, oy+self.h*200),
                          (ox-self.w*300, oy),
                          self.f,
                          stroke_width=[0, 0, 15, 15])
        return im

# Right cheek
class RightCheek(Head):
    def __init__(self, width=1, height=1, fill=(242, 140, 40)):
        self.w = width
        self.h = height
        self.f = fill
    def draw(self, im):
        im = im.copy()
        draw = ImageDraw.Draw(im)
        ox = 1250
        oy = 1900
        self.distorted_ellipse(draw,
                          (ox, oy-self.h*200),
                          (ox+self.w*500, oy+self.h*200),
                          (ox+self.w*300, oy),
                          self.f,
                          stroke_width=[0, 0, 15, 15])
        return im

# Left ear
class LeftEar(Head):
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
        self.distorted_ellipse(draw_mask,
                          (o_ox-self.w*200-self.t*100, o_oy-self.h*700+self.t*200),
                          (o_ox+self.w*600, o_oy+self.h*400),
                          (o_ox-self.t*100, o_oy+self.t*200),
                          "black")
        mask = mask.rotate(self.t*45, fillcolor="white", center=(o_ox, o_oy))
        ear = Image.new("RGBA", im.size, self.o_f)
        draw_ear = ImageDraw.Draw(ear)
        i_ox = 450
        i_oy = 600
        self.distorted_ellipse(draw_ear,
                          (i_ox-(self.t+self.w)*100, i_oy-self.h*400+self.t*200),
                          (i_ox+(1-self.t)*self.w*300, i_oy+self.h*200+self.t*100),
                          (i_ox-self.t*150, i_oy),
                          self.i_f)
        ear = ear.rotate(self.t*45, fillcolor="white", center=(o_ox, o_oy))
        # Perform the composite
        composite = Image.composite(im, ear, mask)
        return composite

# Right ear
class RightEar(Head):
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
        self.distorted_ellipse(draw_mask,
                          (o_ox-self.w*600, o_oy-self.h*700+self.t*200),
                          (o_ox+self.w*200+self.t*100, o_oy+self.h*400),
                          (o_ox+self.t*100, o_oy+self.t*200),
                          "black")
        mask = mask.rotate(self.t*-45, fillcolor="white", center=(o_ox, o_oy))
        ear = Image.new("RGBA", im.size, self.o_f)
        draw_ear = ImageDraw.Draw(ear)
        i_ox = 2050
        i_oy = 600
        self.distorted_ellipse(draw_ear,
                          (i_ox-(1-self.t)*self.w*300, i_oy-self.h*400+self.t*200),
                          (i_ox+(self.t+self.w)*100, i_oy+self.h*200+self.t*100),
                          (i_ox+self.t*150, i_oy),
                          self.i_f)
        ear = ear.rotate(self.t*-45, fillcolor="white", center=(o_ox, o_oy))
        # Perform the composite
        composite = Image.composite(im, ear, mask)
        return composite

# Nose
class Nose(Head):
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
        draw_mask = ImageDraw.Draw(mask)
        # Left eye mask
        self.distorted_ellipse(draw_mask,
                          (eox-self.ew*250, eoy-self.eh*200),
                          (eox+self.ew*250, eoy+self.eh*200),
                          (eox+50, eoy),
                          "black",
                          quadrants=(True, True, False, False))
        self.distorted_ellipse(draw_mask,
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
        draw_mask = ImageDraw.Draw(mask)
        # Left eye mask
        self.distorted_ellipse(draw_mask,
                          (eox-self.ew*250, eoy-self.eh*200),
                          (eox+self.ew*250, eoy+self.eh*200),
                          (eox-50, eoy),
                          "black",
                          quadrants=(True, True, False, False))
        self.distorted_ellipse(draw_mask,
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
