#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *

class ImageScaleWrapper:
    MIN_SHORTER = 1500
    MIN_LONGER = 2000

    def __init__(self, image):
        self._image = image

    def refresh_image_properties(self):
        self.height = self._image.height
        self.width = self._image.width
        self.is_horizontal = self.width > self.height

        self.longer = max(self.width, self.height)
        self.shorter = min(self.width, self.height)

        self.ratio = float(self.longer)/float(self.shorter)

    def is_scalable(self):
        return self.longer > self.MIN_LONGER and self.shorter > self.MIN_SHORTER

    def compute_new_size(self):
        new_longer = self.MIN_LONGER
        new_shorter = float(new_longer) / self.ratio

        if new_shorter < self.MIN_SHORTER:
            new_shorter = 1500
            new_longer = float(new_shorter) * self.ratio

        self.new_longer = int(round(new_longer))
        self.new_shorter = int(round(new_shorter))

        self.new_width = self.new_longer if self.is_horizontal else self.new_shorter
        self.new_height = self.new_shorter if self.is_horizontal else self.new_longer

    def scale(self):
        if not self.is_scalable():
            raise Exception("Image to small")

        self._image.scale(self.new_width, self.new_height)

def scale_image_list(image_list):
    for image in image_list:
        image_wrapper = ImageScaleWrapper(image)
        image_wrapper.refresh_image_properties()

        if not image_wrapper.is_scalable():
            pdb.gimp_message("Image to small!")
            return

        image_wrapper.compute_new_size()
        image_wrapper.scale()


def resize_image_1500_2000():
    pdb.gimp_displays_flush()

    open_images, _ = pdb.gimp_image_list()
    if not open_images:
        pdb.gimp_message("No image!")
        return

    scale_image_list(gimp.image_list())

    pdb.gimp_displays_flush()

register (
    "resize_image_1500_2000",                   # Name registered in Procedure Browser
    "Resize Image 1500 x 2000",                 # Widget title
    "Resize Image 1500 x 2000",                 # Help
    "mwilczek.net",                             # Author
    "mwilczek.net",                             # Copyright Holder
    "2022-11-21",                               # Date
    "Resize Image 1500 x 2000",                 # Menu Entry
    "",                                         # Image Type - No Image Loaded
    [],
    [],
    resize_image_1500_2000,                     # Matches to name of function being defined
    menu = "<Image>/Automation/mwilczek.net"    # Menu Location
)   # End register
#
main()