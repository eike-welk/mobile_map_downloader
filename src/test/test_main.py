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
Test the top level functionality of the map down loader.
"""

from __future__ import division
from __future__ import absolute_import              

#For test modules: ----------------------------------------------------------
#import pytest #contains `skip`, `fail`, `raises`, `config`

import time
import os
import os.path as path
from pprint import pprint


#Set up logging fore useful debug output, and time stamps in UTC.
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.DEBUG)
#Time stamps must be in UTC
logging.Formatter.converter = time.gmtime


def relative_path(*path_comps):
    "Create file paths that are relative to the location of this file."
    return path.abspath(path.join(path.dirname(__file__), *path_comps))


def test_AppMain_parse_aguments():
    "AppMain: test parsing command line arguments"
    from mobile_map_downloader.main import AppMain
    
    print "Start"
    m = AppMain()
    
    func, arg_dict = m.parse_aguments(["lss", "-l"])
    assert func == m.list_server_maps
    assert arg_dict["long_form"] == True
    assert arg_dict["patterns"] == []
    
    func, arg_dict = m.parse_aguments(["lss", "osmand/France*"])
    assert func == m.list_server_maps
    assert arg_dict["long_form"] == False
    assert arg_dict["patterns"] == ["osmand/France*"]
    
    func, arg_dict = m.parse_aguments(["lss", "osmand/France*", "osmand/Germany*"])
    assert arg_dict["patterns"] == ["osmand/France*", "osmand/Germany*"]
    
    func, arg_dict = m.parse_aguments(["-m", "/media/foobar", "lss", "-l", "osmand/France*"])
    assert m.mobile_device == "/media/foobar"
    assert func == m.list_server_maps
    assert arg_dict["long_form"] == True
    assert arg_dict["patterns"] == ["osmand/France*"]
    
    m.parse_aguments(["-h"])
#    m.parse_aguments(["lss", "-h"])
    
    
if __name__ == "__main__":
    test_AppMain_parse_aguments()
    
    pass
