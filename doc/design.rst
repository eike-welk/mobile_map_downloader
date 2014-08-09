##############################################################################
Mobile Map Downloader - Design
##############################################################################

Mobile Map Downloader is a command line program to download maps from the 
Internet and install them on mobile devices, such as smart phones. The program 
is intended to run on a (personal) computer, that has a fast and cheap Internet connection, and a large hard disk. The downloaded maps are also stored on the local computer.

User Interface
===============================================================================

The user interface has sub-commands like, for example, ``git``. The
sub-commands themselves and the logic somewhat resemble ``ftp``. 

Maps are referred to with standardized names. The user does not have to know 
the directories where they are stored, or the different and changing file type
suffixes.

The exact handling of render styles, that are at least supplied by the
OpenAndromaps project, is not yet determined.

Sub-Commands
---------------

lss
    List contents of servers.

lsl
    List locally stored files.

lsd
    List files stored on mobile devices.

install
    Install a map on the mobile device. Downloads the file from the internet
    (only) when needed, because it may be stored locally. 

uninst 
    Delete files on a mobile device.


Major Software components
===============================================================================

The program is divided in four major components: 

Top level
    Contains the user interface, coordinates other components.

Downloader
    Downloads files from a server. Parses the HTML. There is one downloader for
    each server. 

Local Manager
    Manges the local files. Knows the internal structure of the downloaded 
    archives. There is one Local Manager for each server.

Installer
    Installs maps on the mobile device. Knows the directory structure of the
    mobile map viewer program. There is one Installer for each map viewer 
    program.

