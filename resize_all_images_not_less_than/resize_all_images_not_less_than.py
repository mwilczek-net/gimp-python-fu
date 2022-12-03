#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *


DEFAULT_MIN_SHORTER = 1500
DEFAULT_MIN_LONGER = 2000


class ImageScaleWrapper:
    def __init__(self, image, min_shorter, min_longer):
        self._image = image
        self.min_shorter = min_shorter
        self.min_shorter = min_longer

        self.height = None
        self.width = None
        self.is_horizontal = None

        self.longer = None
        self.shorter = None
        self.ratio = None

        self.new_longer = None
        self.new_shorter = None

        self.new_width = None
        self.new_height = None

    def refresh_image_properties(self):
        self.height = self._image.height
        self.width = self._image.width
        self.is_horizontal = self.width > self.height

        self.longer = max(self.width, self.height)
        self.shorter = min(self.width, self.height)

        self.ratio = float(self.longer)/float(self.shorter)

    def is_scalable(self):
        return self.longer > self.min_shorter and self.shorter > self.min_shorter

    def compute_new_size(self):
        new_longer = self.min_shorter
        new_shorter = float(new_longer) / self.ratio

        if new_shorter < self.min_shorter:
            new_shorter = self.min_shorter
            new_longer = float(new_shorter) * self.ratio

        self.new_longer = int(round(new_longer))
        self.new_shorter = int(round(new_shorter))

        self.new_width = self.new_longer if self.is_horizontal else self.new_shorter
        self.new_height = self.new_shorter if self.is_horizontal else self.new_longer

    def scale(self):
        if not self.is_scalable():
            raise Exception("Image to small")

        self._image.scale(self.new_width, self.new_height)


def scale_image_list(image_list, min_shorter, min_longer):
    for image in image_list:
        image_wrapper = ImageScaleWrapper(image, min_shorter, min_longer)
        image_wrapper.refresh_image_properties()

        if not image_wrapper.is_scalable():
            pdb.gimp_message("Image to small!")
            return

        image_wrapper.compute_new_size()
        image_wrapper.scale()


def resize_all_images_not_less_than(min_shorter, min_longer):
    pdb.gimp_displays_flush()

    open_images, _ = pdb.gimp_image_list()
    if not open_images:
        pdb.gimp_message("No images!")
        return

    scale_image_list(gimp.image_list(), min_shorter, min_longer)

    pdb.gimp_displays_flush()

register (
    "resize_all_images_not_less_than",                 # Name registered in Procedure Browser
    "Resize All Image Not Less Than Given Values",     # Widget title
    "Resize All Image Not Less Than Given Values",     # Help
    "mwilczek.net",                                    # Author
    "mwilczek.net",                                    # Copyright Holder
    "2022-11-21",                                      # Date
    "Resize Image Not Less Than",                      # Menu Entry
    "",                                                # Image Type - No Image Loaded
    [
        (PF_INT, "min_shorter", "Shorter edge minimum value (px)", DEFAULT_MIN_SHORTER),
        (PF_INT, "min_longer", "Longer edge minimum value (px)", DEFAULT_MIN_LONGER),
    ],
    [],
    resize_all_images_not_less_than,                   # Matches to name of function being defined
    menu = "<Image>/Automation/mwilczek.net"          # Menu Location
)

main()