#####################
Mobile Map Downloader
#####################

Mobile Map Downloader is a command line program to download maps from the
Internet and install them on mobile devices, such as smart phones. The program
is intended to run on a (personal) computer, that has a fast and cheap Internet
connection, and a large hard disk. The downloaded maps are also stored on the
local computer.

The software is currently in **beta state**. It can be productively used by
adventurous people, or semi experts. Expect it to lack some functionality, to
crash often, and to sometimes do unwanted things.

The program currently only supports **OsmAnd**: http://osmand.net/

The program is written in the **Python** programming language, version **2.7**.
Contributions of code are very welcome. The program has currently only been
tested on **Linux**. It uses however no Linux specific functionality, so
porting to other operating systems should be easy. 


Installation
=======================================

Open a terminal, get administrator/root privileges and type::
    
    pip install mobile-map-download -U

Alternatively you can install the program with Virtualenv, when you don't wand
to use root privileges, and want to delete the program from your computer
without a trace::
    
    virtualenv virtualenv/  #can use any name for the directory
    cd virtualenv/
    source bin/activate
    pip install mobile-map-download -U


Usage
=======================================

List the maps of France, that the program can download::

    dlmap ls "*France*"

Patterns with wildcards should be quoted, because the shell might fill them in. 

Install maps of France for OsmAnd, on a certain device::

    dlmap install "osmand/France*" -m /var/run/media/eike/1A042-B123/
 
The program has a built in help facility, detailed information about its
changing set of features has to be taken from it::

    dlmap -h

Each subcommand has its own help message::

    dlmap install -h

