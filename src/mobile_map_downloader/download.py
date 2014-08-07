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
import lxml.html
import dateutil.parser
from itertools import cycle
import zipfile


#Set up logging fore useful debug output, and time stamps in UTC.
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.DEBUG)
#Time stamps must be in UTC
logging.Formatter.converter = time.gmtime


MapMeta = namedtuple("MapMeta", 
                     "disp_name, tech_name, size, date, description, map_type")
#Some meta data about each map
#    map_type: "osmand" | "mapsforge"

class OsmandDownloader(object):
    """
    Download maps from the servers of the Osmand project.
    """
    list_url = "http://download.osmand.net/list.php"
    
    def __init__(self):
        pass
    
    def get_map_list(self):
        """
        Get list of maps for Osmand that are available for download.
        
        Return
        -------
        
        list[MapMeta]
        
        Note
        ------
        
        The function parses the regular, human readable, HTML document, that
        lists the existing maps for Osmand. It has the following structure:
        
        <html>
            <head> ... </head>
            <body>
                <h1> ... </h1>
                <table>
                    <tr> ... Table headers ... </tr>
                    <tr> ... Nonsense (".gitignore") ... </tr>
                    <tr>
                        <td>
                            <A HREF="/download.php?standard=yes&file=Afghanistan_asia_2.obf.zip">Afghanistan_asia_2.obf.zip</A>
                        </td>
                        <td>03.08.2014</td>
                        <td>8.2</td>
                        <td>
                            Map, Roads, POI, Transport, Address data for 
                            Afghanistan asia
                        </td>
                    </tr>
                    <tr> ... The next map record ... </tr>
                </table>
            </body>
        </html>
        """
        #Download HTML document with list of maps from server of Osmand project
        u = urllib2.urlopen(self.list_url)
        list_html = u.read()
#        print list_html
        #Parse HTML list of maps
        root = lxml.html.document_fromstring(list_html)
        table = root.find(".//table")
        map_metas = []
        for row in table[2:]:
            link = row[0][0]
            map_meta = MapMeta(disp_name = "osmand/" + link.text.split(".")[0], 
                               tech_name = self.list_url + link.get("href"), 
                               size = float(row[2].text), #[MiB]
                               date =  dateutil.parser.parse(row[1].text), 
                               description = row[3].text, 
                               map_type = "osmand")
            map_metas.append(map_meta)
        return map_metas
    
    
    def download_file(self, srv_url, loc_name, disp_name):
        """
        Download a file from the server and store it in the local file system.
        
        Creates a progress animation in the console window, as maps are 
        usually large files.
        
        Arguments
        ---------
        
        srv_url: str
            URL of the file on the remote server.
            
        loc_name: str
            Name of the file in the local file system.
            
        disp_name: str 
            File name for display in the progress bar.
            
        TODO: Dynamically adapt ``buff_size`` so that the animation is updated
              once per second.
        """
        buff_size = 1024 * 50
        backspace = chr(8)
        anim_frames = "/-\-"
        disp_name = disp_name[0:50]
        
        fsrv = urllib2.urlopen(srv_url)
        floc = open(loc_name, "wb")
        
        meta = fsrv.info()
        size_total = int(meta.getheaders("Content-Length")[0])
        size_total_mib = round(size_total / 1024**2, 1)
        size_down = 0
        for frame in cycle(anim_frames):
            #download a piece of the file
            buf = fsrv.read(buff_size)
            if not buf:
                break
            floc.write(buf)
            
            #create progress animation
            size_down += len(buf)
            msg = "{name} : {size} MiB - {proc}%  {anim}".format(
                name=disp_name, size=size_total_mib, 
                proc=round(size_down / size_total * 100), anim=frame)
            msg += backspace * (len(msg) + 1)
            print msg,
        print "{name} : {size} MiB - downloaded".format(
                name=disp_name, size=size_total_mib)
    

        
    