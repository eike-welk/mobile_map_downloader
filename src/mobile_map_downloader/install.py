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
Install maps on a mobile device.
"""

from __future__ import division
from __future__ import absolute_import              

import time
import os
import fnmatch
from os import path
import datetime
from itertools import cycle

from mobile_map_downloader.download import MapMeta


#Set up logging fore useful debug output, and time stamps in UTC.
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.DEBUG)
#Time stamps must be in UTC
logging.Formatter.converter = time.gmtime


class OsmandInstaller(object):
    """
    Install maps for Osmand on the mobile device.
    """
    def __init__(self, device_dir):
        self.device_dir = device_dir
    
    def get_map_list(self):
        """
        List the maps that are installed on the device.
        
        Maps are searched in "``self.device_dir``/osmand".
        
        Return
        -------
        
        list[MapMeta]
        """
        maps_dir = path.join(self.device_dir, "osmand")
        dir_names = os.listdir(maps_dir)
        map_names = fnmatch.filter(dir_names, "*.obf")
        map_names.sort()
        
        map_metas = []
        for name in map_names:
            map_name = path.join(maps_dir, name)
            disp_name = "osmand/" + name.split(".")[0]
            map_size = path.getsize(map_name)
            mod_time = path.getmtime(map_name)
            map_meta = MapMeta(disp_name=disp_name, 
                               tech_name=map_name, 
                               size=map_size, 
                               date=datetime.datetime.fromtimestamp(mod_time), 
                               description="", 
                               map_type="osmand")
            map_metas.append(map_meta)
        
        return map_metas
    
    
    def install_map(self, extractor, disp_name, size_total):
        """
        Install one map file in Osmand's directory on the SD card.
        
        Arguments
        ---------
        
        extractor: file like object
            An object that extracts the map from the zip archive. It behaves
            like a file.
            
        disp_name: str
            Canonical name of the map. The name on the SD card is computed 
            from it.
            
        size_total: int [Bytes]
            The size of the map, uncompressed.
        """
        maps_dir = path.join(self.device_dir, "osmand")
        file_name = disp_name.split("/")[1] + ".obf"
        map_path = path.join(maps_dir, file_name)
        
        buff_size = 1024**2 * 10
        backspace = chr(8)
        anim_frames = "/-\-"
        disp_name = disp_name[0:50]
        size_total_mib = round(size_total / 1024**2, 1)
        
        fsdcard = open(map_path, "wb")
        size_down = 0
        
        for frame in cycle(anim_frames):
            #download a piece of the file
            buf = extractor.read(buff_size)
            if not buf:
                break
            fsdcard.write(buf)
            
            #create progress animation
            size_down += len(buf)
            msg = "{name} : {size} MiB - {proc}%  {anim}".format(
                name=disp_name, size=size_total_mib, 
                proc=round(size_down / size_total * 100), anim=frame)
            msg += backspace * (len(msg) + 1)
            print msg,
            
        fsdcard.close()
        print "{name} : {size} MiB - installed".format(
                name=disp_name, size=size_total_mib)

        
