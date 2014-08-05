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
Download maps from server on the internet.
"""

from __future__ import division
from __future__ import absolute_import              

import time
from collections import namedtuple
import urllib2


#Set up logging fore useful debug output, and time stamps in UTC.
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.DEBUG)
#Time stamps must be in UTC
logging.Formatter.converter = time.gmtime


MapMeta = namedtuple("MapMeta", "disp_name, srv_url, date")
#Some meta data about each map


class OsmandDownloader(object):
    """
    Download maps from the servers of the Osmand project.
    """
    list_url = "http://download.osmand.net/list.php"
    
    def __init__(self):
        pass
    
    def get_map_list(self):
        """
        Get list of maps that are available for download.
        Return: list[MapMeta]
        """
        u = urllib2.urlopen(self.list_url)
        list_html = u.read()
        print list_html
        
        return []
        
        
    def download_file(self, srv_url, loc_name):
        """
        Download a file from the server and store it on the hard drive.
        """
        buff_size = 1024 * 1
        
        u = urllib2.urlopen(srv_url)
        buf = u.read(buff_size)
        print buf
        
        backspace = chr(8)
