# Configuration and Build #

RipTunes does have a long list of pre-requisites, a bit how all open source project does.

The dependencies are:
  1. MinGW - http://sourceforge.net/project/showfiles.php?group_id=2435&package_id=240780
  1. Python 2.6.1 - http://www.python.org/download/releases/2.6.1/
  1. Qt OpenSource - http://qt.nokia.com/downloads
    1. Windows: It is much faster to use the Qt installer.
    1. Linux: It takes a few hours to build on Linux, be patient.
  1. SIP 4.7.9 - http://www.riverbankcomputing.co.uk/software/sip/download
```
  # For Windows, working from C:\tools\sip-4.7.9:
  C:\tools\sip-4.7.9>python configure.py -p win32-g++
  C:\tools\sip-4.7.9>"C:\MinGW\bin\mingw32-make.exe"
  C:\tools\sip-4.7.9>"C:\MinGW\bin\mingw32-make.exe" install

  # For Linux,
  python configure.py
  make
  make install
```
  1. PyQt 4.4.4 - http://www.riverbankcomputing.co.uk/software/pyqt/download
```
  # For windows, the make stage takes a while,
  C:\tools\PyQt-win-gpl-4.4.4>C:\Qt\4.4.3\bin\qtvars.bat
  C:\tools\PyQt-win-gpl-4.4.4>C:\Python26\python.exe configure.py
  C:\tools\PyQt-win-gpl-4.4.4>"C:\MinGW\bin\mingw32-make.exe"
  C:\tools\PyQt-win-gpl-4.4.4>"C:\MinGW\bin\mingw32-make.exe" install

  # For Linux, make sure that the version of Qt you want is in your PATH
  python configure.py
  make
  make install
```
  1. Mutagen 1.18 - http://code.google.com/p/mutagen/
```
  # For Linux,
  python setup.py build
  python setup.py install
```
  1. Add `C:\Qt\4.4.3\bin` in your `PATH` if it's not there.

# Running RipTunes #
### Windows ###
Double click `RipTunes.pyw`
### Linux & Mac ###
`python RipTunes.pyw`