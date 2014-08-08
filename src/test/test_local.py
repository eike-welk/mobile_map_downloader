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
Test the download functions.
"""

from __future__ import division
from __future__ import absolute_import              

#For test modules: ----------------------------------------------------------
#import pytest #contains `skip`, `fail`, `raises`, `config`

import time
import os.path as path
from pprint import pprint
import datetime


#Set up logging fore useful debug output, and time stamps in UTC.
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.DEBUG)
#Time stamps must be in UTC
logging.Formatter.converter = time.gmtime


def relative_path(*path_comps):
    "Create file paths that are relative to the location of this file."
    return path.abspath(path.join(path.dirname(__file__), *path_comps))

    
def test_OsmandManager_get_map_list():
    "Test class OsmandManager: Extracting maps from downloaded archives."
#    #Create the test data
#    #    #File size 0.2 MiB
#    from mobile_map_downloader.download import OsmandDownloader
#    d = OsmandDownloader()
#    srvname = "http://download.osmand.net/download.php?standard=yes&file=Monaco_europe_2.obf.zip"
#    locname = relative_path("../../test_data/maps/osmand/Monaco_europe_2.obf.zip")
#    d.download_file(srvname, locname, "osmand/Monaco_europe_2")
#    #File size 3.0 MiB
#    srvname = "http://download.osmand.net/download.php?standard=yes&file=Jamaica_centralamerica_2.obf.zip"
#    locname = relative_path("../../test_data/maps/osmand/Jamaica_centralamerica_2.obf.zip")
#    d.download_file(srvname, locname, "osmand/Jamaica_centralamerica_2")

    from mobile_map_downloader.local import OsmandManager
    download_dir = relative_path("../../test_data/maps/")
    
    m = OsmandManager(download_dir)
    l = m.get_map_list()
    
    pprint(l)
    assert len(l) == 2
    assert l[0].disp_name == "osmand/Jamaica_centralamerica_2"
    assert l[1].disp_name == "osmand/Monaco_europe_2"


def test_OsmandManager_get_map_extractor():
    """
    OsmandManager: Create an object that extracts a map from one of the 
    downloaded *.zip files.
    """
    from mobile_map_downloader.local import OsmandManager
    
    download_dir = relative_path("../../test_data/maps/osmand/")
    map_path = relative_path("../../test_data/maps/osmand/Jamaica_centralamerica_2.obf.zip")
    
    m = OsmandManager(download_dir)
    fzip, size_total, mod_time = m.get_map_extractor(map_path)
    buf = fzip.read()
    
    print "len(buf):", len(buf)
    print "size_total:", size_total
    print "mod_time:", mod_time
    assert len(buf) == 4518034
    assert len(buf) == size_total
    assert mod_time == datetime.datetime(2014, 8, 3, 15, 10, 2)

    
#def test_OsmandManager_prepare_map():
#    "Test class OsmandManager: Extracting maps from downloaded archives."
#    from mobile_map_downloader.local import OsmandManager
#    
#    print "Start prepare map."
#    in_name = relative_path("../../test_data/maps/osmand/Jamaica_centralamerica_2.obf.zip")
#    out_name = relative_path("../../test_tmp/Jamaica_centralamerica_2.obf.zip")
#    try: os.remove(out_name)
#    except: pass
#    
#    m = OsmandManager("foo")
#    m.prepare_map(in_name, out_name, "osmand/Jamaica_centralamerica_2")
#    
#    #Test name and size of extracted file
#    assert path.isfile(out_name)
#    file_size = path.getsize(out_name)/1024**2
#    print "file size [MiB]:", file_size
#    assert round(file_size, 1) == 4.3
    
    
if __name__ == "__main__":
#    test_OsmandManager_get_map_list()
    test_OsmandManager_get_map_extractor()
#    test_OsmandManager_prepare_map()
    
    pass
