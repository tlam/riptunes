'''
RipTunes transfers songs from iPod to your local machine.
Copyright (C) 2009  Thierry Lam

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import sys
import shutil
import logging
import logging.handlers

from PyQt4 import QtCore
from Tune import *

'''
Browse through the ipod's subfolders and copy the tunes to your local file system
'''
class ManageRip:

    def __init__(self):
        self.logger = logging.getLogger("RipTunesLogger")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.handlers.RotatingFileHandler("log.out", maxBytes=1000000, backupCount=3)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.root_path = self.locate_ipod()

    '''
    Find the ipod music path on the system
    '''
    def locate_ipod(self):
        control_dir = "iPod_Control"
        music_dir = "Music"
        base_path = ""
        platform = sys.platform
        ipod_connected = False

        if platform == "win32":
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            for alpha in alphabet:
                ipod_dir = os.path.join(alpha + ":" + os.sep, control_dir)
                if os.path.isdir(ipod_dir):
                    ipod_connected = True
                    base_path = alpha + ":" + os.sep
                    return os.path.join(base_path, control_dir, music_dir)
            if not ipod_connected:
                return ""
        elif platform == "darwin":
            base_path = "/Volumes"
        elif platform.find("linux") >= 0:
            base_path = "/media"
        else:
            sys.exit("Platform " + platform + " not supported")

        # Process the non-windows ipod_location
        for root, dirs, files in os.walk(base_path):
            for dir in dirs:
                ipod_dir = os.path.join(base_path, dir, control_dir)
                if os.path.isdir(ipod_dir):
                    ipod_connected = True
                    base_path = os.path.join(base_path, dir)
                    return os.path.join(base_path, control_dir, music_dir)
            # Makes sure only the first level of /media or /Volumes are scanned
            break
        
        return ""

    '''
    If the destination directory does not exist, create it
    @param destination_dir, the destination directory to validete
    '''
    def validate_dir(self, destination_dir):
        if not os.path.isdir(destination_dir):
            os.makedirs(destination_dir)

    '''
    Return the number of files on the ipod
    '''
    def numFiles(self):
        numfiles = 0
        for root, dirs, files in os.walk(self.root_path):
            numfiles += len(files)
        return numfiles

    '''
    Return a dictionary of Tunes from by reading all mp3s from root_path.
    The key is the full_path of the tune and associated value is the Tune object
    @param root_path the base location where the mp3s reside
    '''
    def tunes(self, pbar, parent):
        step = 0
        tunes_dict = {}
        numfiles = self.numFiles()
        if self.root_path == "":
            return tunes_dict

        pbar.setMaximum(numfiles)
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if not file.startswith("._"):
                    tune_path = os.path.join(root, file)
                    tune = Tune(tune_path)
                    if tune.valid():
                        tunes_dict[tune_path] = tune
                    else:
                        self.logger.warning("Invalid tune is " + tune_path)
                # Increment the progress bar, processEvents() have to be called on Mac so that the progress can be seen
                step += 1
                pbar.setValue(step)
                parent.getApp().processEvents()
        pbar.setValue(numfiles)
        self.logger.info("Dictionary creation complete")
        return tunes_dict

    '''
    Rip a single tune from it's source location on the ipod to it's destination folder.
    If the destination path does not exist, it will construct it in the following format:
    <base-dest>/<artist>/<tune>
    @param tune, the current Tune to be ripped
    @param base_dest, the base folder destination where the tune will go
    '''
    def rip(self, tune, base_dest):
        # Log full tune path
        self.logger.info("Source: " + tune.full_path())

        destination_dir = os.path.join(base_dest, tune.artist(), tune.album())
        self.validate_dir(destination_dir)
        destination_path = os.path.join(destination_dir, tune.title() + tune.type())

        # Log full destination path
        try:
            self.logger.info("Destination: " + destination_path + "\n")
        except UnicodeEncodeError, msg:
            self.logger.warn("Destination: " + destination_path.encode('utf-8') + "\n")
        shutil.copy(tune.full_path(), destination_path)
