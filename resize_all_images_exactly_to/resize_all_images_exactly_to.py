#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *


DEFAULT_HEIGHT = 225
DEFAULT_WIDTH = 360


class ImageScaleWrapper:
    def __init__(self, image, desired_height, desired_width, warn_if_wrong_ratio):
        self._image = image
        self.desired_height = desired_height
        self.desired_width = desired_width
        self.warn_if_wrong_ratio = warn_if_wrong_ratio

        self.height = None
        self.width = None
        self.ratio = None
        self.desired_ratio = None

    def refresh_image_properties(self):
        self.height = self._image.height
        self.width = self._image.width

        self.ratio = round(float(self.width)/float(self.height), 1)
        self.desired_ratio = round(float(self.desired_width)/float(self.desired_height), 1)
        print("DEBUG Ratios! ", "Current: ", self.ratio, "; Desired: ", self.desired_ratio)

    def is_ratio_ok(self):
        wrong_ratio = self.warn_if_wrong_ratio and self.ratio != self.desired_ratio
        return not wrong_ratio

    def resize(self):
        if not self.is_ratio_ok():
            raise Exception("Image has wrong ratio!")

        self._image.scale(self.desired_width, self.desired_height)


def scale_image_list(image_list, desired_height, desired_width, warn_if_wrong_ratio):
    for image in image_list:
        image_wrapper = ImageScaleWrapper(image, desired_height, desired_width, warn_if_wrong_ratio)
        image_wrapper.refresh_image_properties()

        if not image_wrapper.is_ratio_ok():
            pdb.gimp_message("Image has wrong ratio!")
            continue

        image_wrapper.resize()


def resize_all_images_exactly_to(desired_height, desired_width, warn_if_wrong_ratio):
    pdb.gimp_displays_flush()

    open_images, _ = pdb.gimp_image_list()
    if not open_images:
        pdb.gimp_message("No images!")
        return

    scale_image_list(gimp.image_list(), desired_height, desired_width, warn_if_wrong_ratio)

    pdb.gimp_displays_flush()

register (
    "resize_all_images_exactly_to",                    # Name registered in Procedure Browser
    "Resize All Images Exactly To Given Values",       # Widget title
    "Resize All Images Exactly To Given Values",       # Help
    "mwilczek.net",                                    # Author
    "mwilczek.net",                                    # Copyright Holder
    "2022-11-21",                                      # Date
    "Resize all images exactly to",                    # Menu Entry
    "",                                                # Image Type - No Image Loaded
    [
        (PF_INT, "desired_height", "Height (px)", DEFAULT_HEIGHT),
        (PF_INT, "desired_width", "Width (px)", DEFAULT_WIDTH),
        (PF_BOOL, "warn_if_wrong_ratio", "Warn if source and desired ratios are different", True),
    ],
    [],
    resize_all_images_exactly_to,                      # Matches to name of function being defined
    menu = "<Image>/Automation/mwilczek.net"           # Menu Location
)

main()