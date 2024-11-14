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

        files_to_open = [f for f  in os.listdir(dir_to_open) if not f.startswith('.')]
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


def open_all_files_from_directory(dir_to_open, close_open_images):
    image_opener = ImageOpener()
    image_opener.open_images(dir_to_open, close_open_images)


register (
    "open_all_files_from_directory",                # Name registered in Procedure Browser
    "Open all files from directory",                # Widget title
    "Open all files from directory",                # Help
    "mwilczek.net",                                 # Author
    "mwilczek.net",                                 # Copyright Holder
    "2022-12-03",                                   # Date
    "Open all files from directory",                # Menu Entry
    "",                                             # Image Type - No Image Loaded
    [
        ( PF_DIRNAME, "dir_to_open", "Originals (source) directory:", PICTURES_PATH ),
        ( PF_BOOL, "close_open_images", "Close open images", True),
    ],
    [],
    open_all_files_from_directory,                  # Matches to name of function being defined
    menu = "<Image>/Automation/mwilczek.net"        # Menu Location
)

main()
