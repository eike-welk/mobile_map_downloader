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
Manage local files, that have previously been downloaded.
"""

from __future__ import division
from __future__ import absolute_import              

import time
import os
import fnmatch
from os import path
import zipfile
import datetime

from mobile_map_downloader.download import MapMeta


#Set up logging fore useful debug output, and time stamps in UTC.
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.DEBUG)
#Time stamps must be in UTC
logging.Formatter.converter = time.gmtime


class OsmandManager(object):
    """
    Manage locally stored maps for Osmand.
    """    
    def __init__(self, download_dir):
        self.download_dir = download_dir
        
        #Create own subdir of download dir if it does not exist.
        osmand_dl_dir = path.join(self.download_dir, "osmand")
        if not path.exists(osmand_dl_dir):
            os.mkdir(osmand_dl_dir)
    

    def get_map_list(self):
        """
        Return a list of locally stored maps. Maps are searched in 
        ``self.download_dir``.
        
        Return
        -------
        
        list[MapMeta]
        """
        osmand_dl_dir = path.join(self.download_dir, "osmand")
        dir_names = os.listdir(osmand_dl_dir)
        map_names = fnmatch.filter(dir_names, "*.obf.zip")
        map_names.sort()
        
        map_metas = []
        for name in map_names:
            archive_name = path.join(osmand_dl_dir, name)
            disp_name = "osmand/" + name.split(".")[0]
            _, size_total, date_time = self.get_map_extractor(archive_name)
            map_meta = MapMeta(disp_name=disp_name, 
                               tech_name=archive_name, 
                               size=size_total, 
                               date=date_time, 
                               description="", 
                               map_type="osmand")
            map_metas.append(map_meta)
            
        return map_metas
        
    
    def get_map_extractor(self, archive_path):
        """
        Create file like object, that extracts the map from the zip file.
        Additionally returns some metadata. 
        
        Argument
        --------
        
        archive_path: str
            Path to archive that contains the map.
        
        Returns
        -------
        
        fzip: file like object
            Object that extracts a map from a zip file. Behaves like a file.
            
        size_total: int
            Uncompressed size of the map.
            
        mod_time: date_time.date_time
            Modification time of the map, from the zip archive.
        """
        zip_container = zipfile.ZipFile(archive_path, "r")
#        zip_fnames = zip_container.namelist()
#        print zip_fnames
        zip_finfos = zip_container.infolist()
        zip_fname = zip_finfos[0].filename
        size_total = zip_finfos[0].file_size
        mod_time = datetime.datetime(*zip_finfos[0].date_time)
        fzip = zip_container.open(zip_fname, "r")
        
        return fzip, size_total, mod_time
        
        
#    def prepare_map(self, in_name, out_name, disp_name):
#        """
#        Prepare a map for installation - extract it from the ".zip" archive.
#        
#        The name is chosen to be more generally than "extract", because other
#        map formats might need a different transformation before
#        the maps can be installed on the device.
#        
#        TODO: Only return file like object, the temporary uncompressed 
#              file is unnecessary. 
#              * Open-Andromaps also distributes zip-files with maps
#              * The file system will maybe provide multi threading for free, 
#                when the extracted contents is directly stored on the SD-card. 
#        """
#        buff_size = 1024**2 * 10
#        backspace = chr(8)
#        anim_frames = "/-\-"
#        disp_name = disp_name[0:50]
#        
#        fzip, size_total, _ = self.get_map_extractor(in_name)
#        fext = open(out_name, "wb")
#        size_total_mib = round(size_total / 1024**2, 1)
#        size_down = 0
#        
#        for frame in cycle(anim_frames):
#            #download a piece of the file
#            buf = fzip.read(buff_size)
#            if not buf:
#                break
#            fext.write(buf)
#            
#            #create progress animation
#            size_down += len(buf)
#            msg = "{name} : {size} MiB - {proc}%  {anim}".format(
#                name=disp_name, size=size_total_mib, 
#                proc=round(size_down / size_total * 100), anim=frame)
#            msg += backspace * (len(msg) + 1)
#            print msg,
#        print "{name} : {size} MiB - uncompressed".format(
#                name=disp_name, size=size_total_mib)

        
        
        