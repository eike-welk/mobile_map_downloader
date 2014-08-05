# -*- coding: utf-8 -*-
###############################################################################
#    Mobile Map Downloader - Download maps for your mobile phone.             #
#                                                                             #
#    Copyright (C) 2014 by Eike Welk                                          #
#    eike.welk@gmx.net                                                        #
#                                                                             #
#    License: GPL Version 3                                                   #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
###############################################################################
"""
Test the Osmand specific functions.
"""

from __future__ import division
from __future__ import absolute_import              

#For test modules: ----------------------------------------------------------
import pytest #contains `skip`, `fail`, `raises`, `config`

import time
import os.path as path


#Set up logging fore useful debug output, and time stamps in UTC.
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.DEBUG)
#Time stamps must be in UTC
logging.Formatter.converter = time.gmtime


def relative_path(*path_comps):
    "Create file paths that are relative to the location of this file."
    return path.abspath(path.join(path.dirname(__file__), *path_comps))


def test_OsmandDownloader_get_map_list():
    "Test method OsmandDownloader.get_map_list"
    from mobile_map_downloader.download import OsmandDownloader
    
    d = OsmandDownloader()
    d.get_map_list()
    
    
def test_OsmandDownloader_download_file():
    from mobile_map_downloader.download import OsmandDownloader
    
    url = "http://download.osmand.net/download.php?standard=yes&file=Afghanistan_asia_2.obf.zip"
    d = OsmandDownloader()
    d.download_file(url, None)
    
    
    
if __name__ == "__main__":
    test_OsmandDownloader_get_map_list()
#    test_OsmandDownloader_download_file()
    
    pass
 
