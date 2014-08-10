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
The top level functionality of the map down loader.
"""

from __future__ import division
from __future__ import absolute_import              

import time
import argparse
import sys

from mobile_map_downloader.common import MapMeta
from mobile_map_downloader.download import OsmandDownloader
from mobile_map_downloader.local import OsmandManager
from mobile_map_downloader.install import OsmandInstaller


#Set up logging fore useful debug output, and time stamps in UTC.
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.DEBUG)
#Time stamps must be in UTC
logging.Formatter.converter = time.gmtime

class AppMain(object):
    """Us being good Java citizens. :-)"""
    def __init__(self):
        self.mobile_device = None
        self.downloaders = {"osmand": OsmandDownloader}
#        self.local_managers = [OsmandManager]
#        self.installers = [OsmandInstaller]
    
    def list_server_maps(self, patterns=None, long_form=False):
        """
        List maps that are on servers.
        """
        if not patterns:
            for name in self.downloaders.keys():
                print name
        else:
            pass
    
    def do_nothing_func(self, **args):
        pass

    def parse_aguments(self, cmd_args):
        """Parse the command line arguments"""
        parser = argparse.ArgumentParser(description=
                            "Download and install maps for mobile devices.")
        parser.add_argument("-m", "--mobile_device", metavar="DIR",
                            help="directory that represents the mobile device")
#        parser.add_argument("-v", "--verbose", action="store_true",
#                            help="output additional information for "
#                                 "troubleshooting.")
        subparsers = parser.add_subparsers(
            dest="subcommand", title="Subcommands",
            help='subcommands have an option "-h", for additional help')
        
        lss_parser = subparsers.add_parser(
            "lss", help="list maps on remote servers",
            description="list maps on servers on the Internet")
        lss_parser.add_argument("-l", "--long_form", action="store_true",
                                help="display additional information")
        lss_parser.add_argument("patterns", type=str, nargs="*", metavar="PAT", 
                                help="pattern that selects maps, for example:"
                                     '"osmand/France*", must be quoted')
        
        args = parser.parse_args(cmd_args)
        print args
        
        self.mobile_device = args.mobile_device
        
        if args.subcommand == "lss":
            func = self.list_server_maps
            arg_dict = {"long_form": args.long_form,
                        "patterns": args.patterns}
            return func, arg_dict
        else:
            RuntimeError("Unrecognized subcommand, or missing subcommand.")
        
    def main(self):
        """
        The program's main method.
        """
        func, arg_dict = self.parse_aguments(sys.argv[1:])
        func(**arg_dict)
