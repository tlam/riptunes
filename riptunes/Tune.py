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
import string

from MP3Tag import *
from M4ATag import *

class Tune:

    def __init__(self, tune):
        self.path = tune
        self.extension = os.path.splitext(tune)[-1]
        self.tag = None
        if self.extension == ".mp3":
            self.tag = MP3Tag(tune)
        elif self.extension == ".m4a":
            self.tag = M4ATag(tune)

    def get_tag(self):
        return self.tag

    # Return false if file is not mp3 or m4a
    def valid(self):
        if self.extension == ".mp3":
            return self.tag.valid()
        elif self.tag == None:
            return False
        return True

    def album(self):
        if self.tag.get_album() == "":
            return "UnknownAlbum"
        return self.post(self.tag.get_album())

    def artist(self):
        if self.tag.get_artist() == "":
            return "UnknownArtist"
        return self.post(self.tag.get_artist())

    def title(self):
        if self.tag.get_title() == "":
            return "UnknownTitle"
        return self.post(self.tag.get_title())

    # Return the type of the tune, .m4a or .mp3
    def type(self):
        return self.extension

    # Return the ipod path
    def full_path(self):
        return self.path

    # Replace instances of "/\:" with "-"
    # Replace instances of "?*" with ""
    # Also remove trailing whitespaces
    def post(self, value):
        old = ""
        new = "-"
        if value.find("/") >= 0:
            old = "/"
        elif value.find("\\") >= 0:
            old = "\\"
        elif value.find(":") >= 0:
            old = ":"
        elif value.find("?") >= 0:
            old = "?"
            new = ""
        else:
            old = "*"
            new = ""
        
        return value.replace(old, new).rstrip()
