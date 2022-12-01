#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *
import os


def get_home_path():
    if os.name == 'posix':
        return os.environ['HOME']
    elif os.name == 'nt':
        return os.environ['HOMEPATH']
    else:
        return ""


HOME_PATH = get_home_path()
PICTURES_PATH = os.path.join(HOME_PATH, "Pictures")


class ImageOpener:
    def __init__(self):
        pass

    def open_images(self, dir_to_open, close_open_images):
        if not self.close_open_images(close_open_images):
            return

        files_to_open = os.listdir(dir_to_open)
        for file in files_to_open:
            file_path = os.path.join(dir_to_open, file)
            self._open_image(file_path)

        pdb.gimp_displays_flush()

    def close_open_images(self, close_open_images):
        open_images, _ = pdb.gimp_image_list()
        if close_open_images and open_images > 0:
            pdb.gimp_message("Close all open images first")
            return False
        return True

    def _open_image(self, file_path):
        img = pdb.gimp_file_load(file_path, file_path, run_mode=RUN_INTERACTIVE)
        pdb.gimp_display_new(img)


def open_optionaly_rezise_to_1500_2000(dir_to_open, close_open_images, resize_images):
    image_opener = ImageOpener()
    image_opener.open_images(dir_to_open, close_open_images)

    if resize_images:
        pdb.python_fu_resize_image_1500_2000()
        pdb.gimp_displays_flush()


register (
    "open_optionaly_rezise_to_1500_2000",           # Name registered in Procedure Browser
    "Open And Optionaly Resize to 1500 x 2000",     # Widget title
    "Open And Optionaly Resize to 1500 x 2000",     # Help
    "mwilczek.net",                                 # Author
    "mwilczek.net",                                 # Copyright Holder
    "2022-11-21",                                   # Date
    "Open & Optionaly Resize to 1500 x 2000",       # Menu Entry
    "",                                             # Image Type - No Image Loaded
    [
        ( PF_DIRNAME, "dir_to_open", "Originals (source) directory:", PICTURES_PATH ),
        ( PF_BOOL, "close_open_images", "Close open images", True),
        ( PF_BOOL, "resize_images", "Resize images to 1500x2000", False),
    ],
    [],
    open_optionaly_rezise_to_1500_2000,             # Matches to name of function being defined
    menu = "<Image>/Automation/mwilczek.net"        # Menu Location
)

main()