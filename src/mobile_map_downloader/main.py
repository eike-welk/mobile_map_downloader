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
import fnmatch
import os.path as path
import os

from mobile_map_downloader.common import MapMeta, items_sorted
from mobile_map_downloader.download import OsmandDownloader
from mobile_map_downloader.local import OsmandManager
from mobile_map_downloader.install import OsmandInstaller


#Set up logging fore useful debug output, and time stamps in UTC.
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.DEBUG)
#Time stamps must be in UTC
logging.Formatter.converter = time.gmtime


class AppHighLevel(object):
    """
    High level operations of the program, that are not directly relates to the 
    user interface.  
    """
    app_directory_choices = ["~/Downloads/mobile_map_downloader", 
                             "~/mobile_map_downloader"]
    def __init__(self):
        self.app_directory = None
        self.mobile_device = None
        #Low level components
        self.downloaders = {}
        self.local_managers = {}
        self.installers = {}

    def create_low_level_components(self, app_directory = None, 
                                    mobile_device = None):
        """
        Create low level components that do the real work. 
        Must be called before the application can do anything useful.
        
        Some components need additional resources:
        
        * ``self.local_managers`` need a writable directory to store downloaded
          files. Its path is in ``self.app_directory``. This function searches
          for this directory, and create it when none is found.
          
        * ``self.installers`` need a path to a mobile device in 
          ``self.mobile_device``. 
        """
        #Init with predefined values for more easy testing.
        if app_directory:
            self.app_directory = app_directory
        if mobile_device:
            self.mobile_device = mobile_device
            
        #Create the low level components
        self.downloaders = {"osmand": OsmandDownloader()}
        
        if not self.find_app_directory():
            self.create_app_directory()
        if self.app_directory:
            self.local_managers = {"osmand": OsmandManager(self.app_directory)}
        else:
            print "No writable download directory! No downloads are possible."
            
        if self.mobile_device:
            self.installers = {"osmand": OsmandInstaller(self.mobile_device)}
        else:
            print "No mobile device!"
        
    def find_app_directory(self):
        """
        Find the directory of the program.
        
        Do this portably with:
            https://pypi.python.org/pypi/appdirs/1.2.0
        """
        if self.app_directory:
            return self.app_directory
        for app_dir in self.app_directory_choices:
            app_dir = path.expanduser(app_dir)
            if path.isdir(app_dir):
                self.app_directory = app_dir
                return app_dir
        return None
        
    def create_app_directory(self):
        """Create a directory for the program."""
        for app_dir in self.app_directory_choices:
            app_dir = path.expanduser(app_dir)
            root, _ = path.split(app_dir)
            if path.isdir(root):
                os.mkdir(app_dir)
                self.app_directory = app_dir
                return app_dir
        return None
        
    def get_filtered_map_list(self, lister_dict, patterns):
        """
        Create a list of maps, that match certain patterns.
        
        Arguments
        ----------
        
        lister_dict: dict[str:object]
            Object must have a method ``get_map_list() -> [MapMeta]``.
        
        patterns: list[str]
            List of shell wildcard patterns.
            
        Retuns
        --------
        
        list[MapMeta]
        """
        #Get listing of all maps of all servers.
        all_maps = []
        for _, downloader in items_sorted(lister_dict):
            maps = downloader.get_map_list()
            all_maps += maps
        #Filter the names for the patterns.
        all_matches = []
        for pattern in patterns:
            all_matches += [map_ for map_ in all_maps 
                            if fnmatch.fnmatchcase(map_.disp_name, pattern)]
        return all_matches


class ConsoleAppMain(object):
    """Us being good Java citizens. :-)"""
    def __init__(self):
        self.app = AppHighLevel()
         
    def print_summary_list(self, lister_dict, long_form):
        """
        Print a summary list of maps.
        
        * lister_dict: dict[str:object]
        * long_form: bool
        """
        for name, lister in items_sorted(lister_dict):
            maps = lister.get_map_list()
            size_total = 0
            for map_ in maps:
                size_total += map_.size
            print "{name:<20} {n:>4} files, {size:3.1f} GiB".format(
                        name=name, n=len(maps), size=size_total / 1024**3)
            if long_form:
                try:
                    print "    URL: {url}".format(url=lister.list_url)
                except AttributeError:
                    pass

    def print_regular_list(self, lister_dict, patterns):
        """
        Print regular list of maps.
        
        * lister_dict: dict[str:object]
        * patterns: list[str]
         """
        maps = self.app.get_filtered_map_list(lister_dict, patterns)
        size_total = 0
        for map_ in maps:
            print "{name:<65} {size:3.3f} Gib".format(
                        name=map_.disp_name, size=map_.size / 1024**3)
            size_total += map_.size
        print "-" * 79
        print " " * 56 + "{num} files, {size:3.3f} GiB".format(
                        num=len(maps), size=size_total / 1024**3)

    def list_server_maps(self, patterns=None, long_form=False):
        """
        List maps that are on servers. Performs ``lss`` subcommand.
        """
        if not patterns:
            self.print_summary_list(self.app.downloaders, long_form)
        else:
            self.print_regular_list(self.app.downloaders, patterns)

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
            help='all subcommands have an option "-h", for additional help')
        
        lss_parser = subparsers.add_parser(
            "lss", help="list maps on servers on the Internet",
            description="list maps on servers on the Internet")
        lss_parser.add_argument("-l", "--long_form", action="store_true",
                                help="display additional information")
        lss_parser.add_argument("patterns", type=str, nargs="*", metavar="PAT", 
                                help="pattern that selects maps, for example:"
                                     '"osmand/France*", must be quoted')
        
        args = parser.parse_args(cmd_args)
        print args
        
        self.app.mobile_device = args.mobile_device
        
        if args.subcommand == "lss":
            func = self.list_server_maps
            arg_dict = {"long_form": args.long_form,
                        "patterns": args.patterns}
            return func, arg_dict
        else:
            RuntimeError("Unrecognized subcommand.")
        
    def main(self):
        """
        The program's main method.
        """
        func, arg_dict = self.parse_aguments(sys.argv[1:])
        self.app.create_low_level_components()
        func(**arg_dict) #IGNORE:W0142
