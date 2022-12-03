#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *
import os

DEFAULT_MIN_SHORTER = 1500
DEFAULT_MIN_LONGER = 2000

def get_home_path():
    if os.name == 'posix':
        return os.environ['HOME']
    elif os.name == 'nt':
        return os.environ['HOMEPATH']
    else:
        return ""


HOME_PATH = get_home_path()
PICTURES_PATH = os.path.join(HOME_PATH, "Pictures")


def open_images_optionaly_rezise_not_less_than(dir_to_open, close_open_images, resize_images, min_shorter, min_longer):
    pdb.python_fu_open_all_files_from_directory(dir_to_open, close_open_images)

    if resize_images:
        pdb.python_fu_resize_all_images_not_less_than(min_shorter, min_longer)


register (
    "open_images_optionaly_rezise_not_less_than",               # Name registered in Procedure Browser
    "Open And Optionaly Resize Not Less Than Given Values",     # Widget title
    "Open And Optionaly Resize Not Less Than Given Values",     # Help
    "mwilczek.net",                                             # Author
    "mwilczek.net",                                             # Copyright Holder
    "2022-11-21",                                               # Date
    "Open & optionaly resize not less than given values",       # Menu Entry
    "",                                                         # Image Type - No Image Loaded
    [
        (PF_DIRNAME, "dir_to_open", "Originals (source) directory:", PICTURES_PATH),
        (PF_BOOL, "close_open_images", "Close open images", True),
        (PF_BOOL, "resize_images", "Resize images to 1500x2000", True),
        (PF_INT, "min_shorter", "Shorter edge minimum value (px)", DEFAULT_MIN_SHORTER),
        (PF_INT, "min_longer", "Longer edge minimum value (px)", DEFAULT_MIN_LONGER),
    ],
    [],
    open_images_optionaly_rezise_not_less_than,                 # Matches to name of function being defined
    menu = "<Image>/Automation/mwilczek.net"                    # Menu Location
)

main()