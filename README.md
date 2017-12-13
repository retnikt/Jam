# jamm
(formerly Jam)  
A linux macro tool for über-nerds, productivity porn-stars, and, like, I dunno, stage lighting operators? 

*Not to be confused with [Jam](https://lets-jam.org) or [Jam STAPL](https://www.altera.com/support/support-resources/download/programming/jam.html)*

[Click here to skip to the Installation section](#installation)

You can remap almost ANY input:
 - ~~Additional Keyboards, mice, etc.~~ NOT YET IMPLEMENTED
 - MIDI devices
 - ~~USB/Serial devices (e.g. Arduinos)~~ NOT YET IMPLEMENTED
 - ~~TCP clients (even with encryption!)~~ NOT YET IMPLEMENTED
 - ~~A customisable HTTP interface (e.g. for mobile devices)~~ NOT YET IMPLEMENTED
 
to almost anything else:
 - Console commands
 - ~~Other key combinations~~ NOT YET IMPLEMENTED
 - ~~File operations~~ NOT YET IMPLEMENTED

## About
jamm (formerly Jam) is a scripting language similar to 
[AutoHotKey](https://autohotkey.com), based on XML.  
Not to be confused with [Jam](https://lets-jam.org) or [Jam STAPL](https://www.altera.com/support/support-resources/download/programming/jam.html)
### Rationale
This is a tool for linux because there are loads of
similar Windows alternatives, but very few equivalents
for linux. Maybe in the future I will release a Windows
version, but it would require a significant rewrite.

Python 2 is not supported, and never will be, because 
[it will not be maintained past 2020.](https://pythonclock.org)
### Acknowledgements
 - [Tom Scott](https://tomscott.com), for [this video](https://youtu.be/lIFE7h3m40U)
 - [Taran Van Hemert](https://twitter.com/TaranVH), for his obsession with macros
## Installation
### Requirements
 - A recent linux OS (must be a Debian, Red Hat, or Arch derivative)
 - [python](https://python.org) >=3.2 **with compiled-in `complex` support**: 
 Pre-installed on most systems. Also available in most package managers.
 - [xdotool](https://www.semicomplete.com/projects/xdotool/semicomplete.com/projects/xdotool)
 Version 3.x: **IMPORTANT NOTE**: The version on the 
 website is only version 2. I am not sure where source files for
 version 3 are, but most package managers have them.
 - [python3-lxml](https://lxml.de): Pre-installed on some systems.
 Also available [on PyPI](https://pypi.python.org/pypi/lxml/4.1.1) 
 and most package managers.
 - [python-evdev](https://python-evdev.readthedocs.io): Available
 through most package managers and [on PyPI](https://pypi.python.org/pypi/evdev)
 
## Contributing
Don't.  
