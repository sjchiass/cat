import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.patches as mpatches

from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox, TransformedBbox
from matplotlib.legend_handler import HandlerBase

from catlib import *

# https://stackoverflow.com/questions/26029592/insert-image-in-matplotlib-legend
class ImageHandler(HandlerBase):
    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize,
                       trans):

        # create a bounding box to house the image
        bb = Bbox.from_bounds(xdescent,
                              ydescent-width/2,
                              width,
                              width)

        tbb = TransformedBbox(bb, trans)
        image = BboxImage(tbb)
        image.set_data(self.image_data)

        self.update_prop(image, orig_handle, legend)

        return [image]

    def set_image(self, pattern, mood):
        self.image_data = np.array(draw_cat(pattern, mood, 100))

# A simple function which should be added to the main part of the catlib
def draw_cat(pattern, mood, size):
    cat = [Head(),
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
    image = Image.new("RGBA", (size, size), (255, 0, 0, 0))

    for x in cat:
        image = x.set_pattern(pattern).set_mood(mood).draw(image)

    return image

# https://stackoverflow.com/questions/2318288/how-to-use-custom-png-image-marker-with-plot
def plot_cat_markers(x: list,
                     y: list,
                     s: list,
                     p: list,
                     m: list,
                     ax: plt.Axes = None) -> None:
    """Draw cat markers with patterns and moods

    Args:
        x (list): Array of x values
        y (list): Array of y values
        s (list): Array of marker sizes
        p (list): Array of patterns to use
        m (list): Array of moods to use
        ax (plt.Axes, optional): a pyploy Axe instancs, otherwise defaults to plt.gca()

    Raises:
        ValueError: x, y, s, p and m are not all the same length
    """                     
    ax = ax or plt.gca()

    if len(x) == len(y) == len(s) == len(p) == len(m):
        # All the arrays should be the same length
        pass
    else:
        raise ValueError("x, y, s, p and m are not all the same length")

    for xval, yval, size, pattern, mood in zip(x, y, s, p, m):

        im = OffsetImage(draw_cat(pattern, mood, 100),
        zoom=size*36/(ax.figure.dpi))
        im.image.axes = ax

        ab = AnnotationBbox(im, (xval, yval), frameon=False, pad=0.0,)

        ax.add_artist(ab)


def create_cat_legend(pattern_values: list,
                      mood_values: list,
                      labels: list,
                      ax: plt.Axes = None) -> None:
    """Wraps around a call to ax.legend() so that cats logo appear in the legend.

    Args:
        pattern_values (list): array of patterns applied to the data
        mood_values (list): array of moods applied to the data
        labels (list): labels or categories for all datapoints
        ax (plt.Axes, optional): a pyploy Axe instancs, otherwise defaults to plt.gca()
    """
    ax = ax or plt.gca()

    # The legend will only show unique combinations of markers and labels
    unique_cats = list(
        set([(p, m) for p, m in zip(pattern_values, mood_values)]))
    unique_labels = list(set(labels))
    unique_combos = list(
        set([(p, m, l) for p, m, l in zip(pattern_values, mood_values, labels)]))

    if len(unique_cats) == len(unique_cats) == len(unique_combos):
        # This is fine. Cats and labels will not repeat in the legend.
        pass
    else:
        print("Warning: there are duplicates in the legend.")

    legend_dict = [{"pattern": x[0], "mood": x[1], "label": x[2]}
                   for x in unique_combos]

    # The handles are just labels
    l = [mpatches.Patch(label=c["label"]) for c in legend_dict]

    # Each handle (label) needs a handler that supports images
    h = [ImageHandler() for x in legend_dict]
    for hamp, combo in zip(h, legend_dict):
        hamp.set_image(pattern=combo["pattern"], mood=combo["mood"])
    h = {li: hi for li, hi in zip(l, h)}

    ax.legend(handles=l, handler_map=h)

# # Example
# x = np.random.rand(25)
# y = np.random.rand(25)
# s = np.random.rand(25)
# p = np.random.choice(list(Head().pattern_dict.keys())[:2], 25)
# m = np.random.choice(list(Head().mood_dict.keys())[:2], 25)
# l = [f"{p}+{m}" for p, m in zip(p, m)]

# fig, ax = plt.subplots()
# ax.scatter(x, y, fc="None", ec="None")
# plot_cat_markers(x, y, s, p, m, ax=ax)
# create_cat_legend(p, m, l)

# plt.show()
