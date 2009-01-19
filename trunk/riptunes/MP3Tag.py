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

import mutagen

from mutagen.mp3 import MP3

class MP3Tag:

    def __init__(self, tune):
        try:
            self.id3info = MP3(tune)
        except UnicodeEncodeError, msg:
            self.id3info = None
            print msg
        except mutagen.id3.ID3NoHeaderError, msg:
            self.id3info = None
            print msg
        except ValueError, msg:
            self.id3info = None
            print msg

    def info(self):
        return self.id3info

    def valid(self):
        if self.id3info == None:
            return False
        return True

    def get_album(self):
        if self.id3info.has_key("TALB"):
            return self.id3info["TALB"][0]
        else:
            return ""

    def get_artist(self):
        if self.id3info.has_key("TPE1"):
            return self.id3info["TPE1"][0]
        elif self.id3info.has_key("TPE2"):
            return self.id3info["TPE2"][0]
        else:
            return ""

    def get_title(self):
        if self.id3info.has_key("TIT2"):
            return self.id3info["TIT2"][0]
        else:
            return ""
