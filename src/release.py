"""
===============================================================================
Create a release of "mobile_map_downloader". Upload files and metadata to PyPi.
===============================================================================

This script can be used to automate the release of new versions of the
"mobile_map_downloader" project, but it should also serve as documentation 
for the somewhat complex release process.

The PyPi site for "mobile_map_downloader" is at:
   https://pypi.python.org/pypi/mobile_map_downloader

Usage
======

The script has several options.

At the beginning of the release process you might want to run::

    python release.py -s
    
This stores your PyPi user name and password in "~/.pypirc". This step is not
necessary to make releases, but is convenient if you need several attempts to 
get the release right. If user name and password are not stored in 
"~/.pypirc" Python's upload machinery will ask for them.

To upload metadata and files to PyPi run::

    python release.py -u
    
To clean up after a release, run::
    
    python release.py -c
    
This option deletes the "~/.pypirc" file.
"""

import argparse
import getpass
import os
import os.path as path 
import textwrap
import shutil
import subprocess 

import mob_map_dl.common


def relative(*path_fragments):
    'Create a file path that is relative to the location of this file.'
    return path.abspath(path.join(path.dirname(__file__), *path_fragments))

def make_release_tag():
    "Create the relese tag from the version string"
    return "release-" + mob_map_dl.common.VERSION

def is_good_version():
    """
    Check program version and related Git tags. 
    Returns False if version already exists, returns True otherwise.
    """
    git_tag_out = subprocess.check_output(["git", "tag"])
    tags = git_tag_out.split("\n") #IGNORE:E1103
    if make_release_tag() in tags:
        return False
    else:
        return True


#Parse the command line arguments of the release script
parser = argparse.ArgumentParser(description=
    'Upload a new version of "mobile_map_download" to PyPi.')

parser.add_argument('-s, --start', dest='start', action='store_true',
                    help='Start the release process. '
                         'Temporarily store password and user name for PyPi '
                         'in "~/.pypirc".')
parser.add_argument('-u, --upload', dest='upload', action='store_true',
                    help='Upload files and metadata to PyPi.')
parser.add_argument('-c, --cleanup', dest='cleanup', action='store_true',
                    help='Cleanup after the release. '
                         'Especially remove "~/.pypirc".')

args = parser.parse_args()


#Do some necessary computations and checks
homedir = path.expanduser("~")
pypirc_path = path.join(homedir, ".pypirc")
if path.exists(pypirc_path):
    print ('"~/.pypirc" file exists. '
           'Delete it with "release -c" when you are done.\n')


#Default action: display help message. ----------------------------------------
if not (args.start or args.upload or args.cleanup):
    print "No action selected. You must select at least one action/option.\n"
    parser.print_help()
    exit(0)


#Start the release process ----------------------------------------------------
if args.start:
    #Create a ".pypirc" file 
    print 'Store PyPi username and password temporarily in "~/.pypirc" file.'
    username = raw_input("PyPi username:")
    password = getpass.getpass('PyPi password:')
    pypirc_text = textwrap.dedent(
        """
        [distutils]
        index-servers = 
            pypi
        
        [pypi]
        #repository: http://www.python.org/pypi
        username:{u}
        password:{p}
        """.format(u=username, p=password))
    with open(pypirc_path, "w") as pypirc_file:
        pypirc_file.write(pypirc_text)

    #Remind of necessary actions, that are easily forgotten. 
    print '\n=================================================='
    if not is_good_version():
        print "* Release '{}' already exists!".format(make_release_tag())
        print "* Please increase the version."
        print "*"
    print '* Please run the tests before uploading a release.'
    print '==================================================\n'


#Do the release ---------------------------------------------------------------
if args.upload:
    if not is_good_version():
        print "Release '{}' already exists!".format(make_release_tag())
        print "Please increase the version."
        print "Exiting."
        exit(1)
        
    #Copy ``README.rst`` from the upper level directory.
    shutil.copy(relative("..", "README.rst"), relative("README.rst"))
        
    #Build source distribution, upload metadata, upload distribution(s)
    subprocess.check_call(["python", "setup.py",
                           "sdist", 
                           "register", "-r", "pypi", 
                           "upload", "-r", "pypi",])
    #Create a new release tag
    subprocess.check_call(["git", "tag", make_release_tag()])


#Clean up from the release process. -------------------------------------------
if args.cleanup:
    things_done = 0

    #Remove the ".pypirc" file.
    if path.exists(pypirc_path):
        print 'Removing "~/.pypirc".'
        os.remove(pypirc_path)
        things_done += 1

    #Remove ``README.rst`` from this directory
    if path.exists(relative("README.rst")):
        print 'Removing "README.rst"'
        os.remove(relative("README.rst"))
        things_done += 1

    if things_done == 0:
        print 'Nothing to do.'

