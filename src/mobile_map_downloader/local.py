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

from mobile_map_downloader.common import MapMeta


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
    def __init__(self, download_dir_root):
#        self.download_dir_root = download_dir_root
        self.download_dir = path.join(download_dir_root, "osmand")
        
        #Create own subdir of download dir if it does not exist.
        if not path.exists(self.download_dir):
            os.mkdir(self.download_dir)
    

    def make_disp_name(self, file_name_path):
        """
        Create a canonical name from a file name or path of a locally stored
        zipped map. 
        The canonical name is used in the user interface.
        
        The canonical name has the form:
            "osmand/Country_Name.obf" or
            "osmand/Language.voice"
        """
        _, file_name = path.split(file_name_path)
        disp_name = "osmand/" + file_name.rsplit(".", 1)[0]
        return disp_name
    
    def make_full_name(self, disp_name):
        """
        Create a path to a locally stored map from its canonical name. 
        """
        _, fname = path.split(disp_name)
        full_name = path.join(self.download_dir, fname + ".zip")
        return full_name
    
    def get_map_list(self):
        """
        Return a list of locally stored maps. Maps are searched in 
        ``self.download_dir``.
        
        Return
        -------
        
        list[MapMeta]
        """
        dir_names = os.listdir(self.download_dir)
        map_names = fnmatch.filter(dir_names, "*.obf.zip")
        map_names.sort()
        
        map_metas = []
        for name in map_names:
            archive_name = path.join(self.download_dir, name)
            disp_name = self.make_disp_name(name)
            _, size_total, date_time = self.get_map_extractor(archive_name)
            map_meta = MapMeta(disp_name=disp_name, 
                               full_name=archive_name, 
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
        
        