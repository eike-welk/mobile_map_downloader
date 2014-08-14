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
import shutil
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


def create_writable_test_dirs(idx):
    """
    Create temporary writable directories with test data. Different names 
    for each test enable parallel execution of tests.
    
    The following directories are created:
    
    "../../test_tmp/mobile_map_downloader" + idx 
        Application directory with test data.
        
    "../../test_tmp/TEST-DEVICE" + idx
        Device directory  with test data.
    """
    idx = str(idx)
    test_app_dir = relative_path("../../test_tmp/mobile_map_downloader" + idx)
    test_dev_dir = relative_path("../../test_tmp/TEST-DEVICE" + idx)
    shutil.rmtree(test_app_dir, ignore_errors=True)
    shutil.rmtree(test_dev_dir, ignore_errors=True)
    shutil.copytree(relative_path("../../test_data/maps"), test_app_dir)
    shutil.copytree(relative_path("../../test_data/TEST-DEVICE1"), test_dev_dir)
    return test_app_dir, test_dev_dir
    
#--- AppHighLevel
def test_AppHighLevel_get_filtered_map_list():
    "AppHighLevel: test get_filtered_map_list()"
    from mobile_map_downloader.main import AppHighLevel
    
    print "Start"
    app = AppHighLevel()
    app.create_low_level_components(
                app_directory=relative_path("../../test_data/maps"),
                mobile_device=relative_path("../../test_data/TEST-DEVICE1"))
    
    #List maps on remote servers whose names contain the word "Monaco".
    maps = app.get_filtered_map_list(app.downloaders, ["*Monaco*"])
    pprint(maps)
    assert len(maps) == 1
    assert maps[0].disp_name == "osmand/Monaco_europe_2.obf"
    assert maps[0].full_name.find("download.osmand.net") > 0
    
    #List all locally downloaded maps.
    maps = app.get_filtered_map_list(app.local_managers, ["*"])
    pprint(maps)
    assert len(maps) == 2
    assert maps[0].disp_name == "osmand/Jamaica_centralamerica_2.obf" 
    assert maps[1].disp_name == "osmand/Monaco_europe_2.obf"
    assert maps[0].full_name.find("test_data/maps") > 0
    
    #List all maps that are installed on the current device.
    maps = app.get_filtered_map_list(app.installers, ["*"])
    pprint(maps)
    assert len(maps) == 2
    assert maps[0].disp_name == "osmand/Jamaica_centralamerica_2.obf" 
    assert maps[1].disp_name == "osmand/Monaco_europe_2.obf"
    assert maps[0].full_name.find("test_data/TEST-DEVICE1") > 0
    

def test_AppHighLevel_plan_work():
    "AppHighLevel: test plan_work"
    from datetime import datetime
    from mobile_map_downloader.common import MapMeta
    from mobile_map_downloader.main import AppHighLevel
    
    print "Start"
    #Create source and destination lists
    src = [MapMeta("map1", "f/map1", 1, datetime(2000, 1, 1), "foo", "bar"),
           MapMeta("map2", "f/map2", 1, datetime(2000, 1, 1), "foo", "bar"),
           MapMeta("map3", "f/map3", 1, datetime(2000, 1, 1), "foo", "bar")]
    dst = [MapMeta("map1", "f/map1", 1, datetime(2000, 1, 1), "foo", "bar"),
           MapMeta("map2", "f/map2", 1, datetime(1999, 1, 1), "foo", "bar")]
    
    app = AppHighLevel()
    
    work = app.plan_work(src, dst, "only_missing")
    pprint(work)
    assert len(work) == 1
    assert work[0].disp_name == "map3"
    
    work = app.plan_work(src, dst, "replace_newer")
    pprint(work)
    assert len(work) == 2
    assert work[0].disp_name == "map2"
    assert work[1].disp_name == "map3"
    
    work = app.plan_work(src, dst, "replace_all")
    pprint(work)
    assert len(work) == 3

    
def test_AppHighLevel_download_file():
    "AppHighLevel: test download_file()"
    from mobile_map_downloader.main import AppHighLevel
    from mobile_map_downloader.common import MapMeta
    
    print "Start"
    app_directory, mobile_device = create_writable_test_dirs("m1")    
    file_meta = MapMeta(disp_name="osmand/Cape-verde_africa_2.obf", 
                        full_name="http://download.osmand.net/download.php?standard=yes&file=Cape-verde_africa_2.obf.zip", 
                        size=None, time=None, description=None, map_type=None)
    
    app = AppHighLevel()
    app.create_low_level_components(app_directory, mobile_device)
    
    app.download_file(file_meta)
    
    assert path.isfile(path.join(app_directory, 
                                 "osmand/Cape-verde_africa_2.obf.zip"))
    
    
def test_AppHighLevel_install_file():
    "AppHighLevel: test install_file()"
    from mobile_map_downloader.main import AppHighLevel
    from mobile_map_downloader.common import MapMeta
    
    print "Start"
    app_directory, mobile_device = create_writable_test_dirs("m2")
    file_meta = MapMeta(disp_name="osmand/Jamaica_centralamerica_2.obf", 
                        full_name=path.join(
                                    app_directory, 
                                    "osmand/Jamaica_centralamerica_2.obf.zip"), 
                        size=None, time=None, description=None, map_type=None)
    #Remove file that will be created though install algorithm
    os.remove(path.join(mobile_device, "osmand/Jamaica_centralamerica_2.obf"))
    
    app = AppHighLevel()
    app.create_low_level_components(app_directory, mobile_device)
    
    app.install_file(file_meta)
    
    assert path.isfile(path.join(mobile_device, 
                                 "osmand/Jamaica_centralamerica_2.obf"))
    
    
def test_AppHighLevel_download_install():
    "AppHighLevel: test get_filtered_map_list()"
    from mobile_map_downloader.main import AppHighLevel
    
    print "Start"
    app_directory, mobile_device = create_writable_test_dirs("m3")
    
    app = AppHighLevel()
    app.create_low_level_components(app_directory, mobile_device)
    
    app.download_install(["*Monaco*", "*Faroe-islands*"], mode="only_missing")
    
    assert path.isfile(path.join(app_directory, "osmand", 
                                 "Faroe-islands_europe_2.obf.zip"))
    assert path.isfile(path.join(mobile_device, "osmand", 
                                 "Faroe-islands_europe_2.obf"))
    
#--- ConsoleAppMain
def test_ConsoleAppMain_list_server_maps():
    "ConsoleAppMain: test listing maps on remote servers"
    from mobile_map_downloader.main import ConsoleAppMain
    
    print "Start"
    m = ConsoleAppMain()
    m.app.create_low_level_components(
                        app_directory=relative_path("../../test_data/maps"))
    
    m.list_server_maps([], long_form=True)
    print 
    m.list_server_maps(["osmand/France*", "osmand/Germany*"], long_form=False)
    
    
def test_ConsoleAppMain_parse_aguments():
    "ConsoleAppMain: test parsing command line arguments"
    from mobile_map_downloader.main import ConsoleAppMain
    
    print "Start"
    m = ConsoleAppMain()
    
    # lss ---------------------------------------------
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
    assert m.app.mobile_device == "/media/foobar"
    assert func == m.list_server_maps
    assert arg_dict["long_form"] == True
    assert arg_dict["patterns"] == ["osmand/France*"]
    
    # lss ---------------------------------------------
    func, arg_dict = m.parse_aguments(["install", "osmand/France*"])
    assert func == m.download_install
    assert arg_dict["patterns"] == ["osmand/France*"]
    assert arg_dict["mode"] == "only_missing"
    
    func, arg_dict = m.parse_aguments(["install", "osmand/France*", "-u"])
    assert func == m.download_install
    assert arg_dict["mode"] == "replace_newer"
    
    func, arg_dict = m.parse_aguments(["install", "osmand/France*", "-f"])
    assert func == m.download_install
    assert arg_dict["mode"] == "replace_all"
    
#    #Must raise exception & print help message
#    func, arg_dict = m.parse_aguments(["install"])
    
#    m.parse_aguments(["-h"])
#    m.parse_aguments(["lss", "-h"])
    
    
if __name__ == "__main__":
#    test_AppHighLevel_get_filtered_map_list()
#    test_AppHighLevel_download_file()
#    test_AppHighLevel_install_file()
#    test_AppHighLevel_plan_work()
#    test_AppHighLevel_download_install()
#    test_ConsoleAppMain_list_server_maps()
    test_ConsoleAppMain_parse_aguments()
    
    pass