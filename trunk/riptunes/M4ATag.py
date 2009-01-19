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

from mutagen.mp4 import MP4, MP4Info

class M4ATag(dict):

    def __init__(self, pathname=None):
        super(dict, self).__init__()
        if pathname is None: return
        self.info = MP4(pathname)

    def get_album(self):
        return self.info['\xa9alb'][0]

    def get_artist(self):
        return self.info['\xa9ART'][0]

    def get_title(self):
        return self.info['\xa9nam'][0]
