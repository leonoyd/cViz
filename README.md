# CallGr

Generates a call graph from information obtain during the GCC compilation process.

CallGr is intended to give its user a high level "birds eye view" of the entire codebase or a subsection.

# Installation

## Prerequisites

The program is not a self contained program. It works by calling two other programs, both of which need to be installed on your
operating system.

Assuming an Ubuntu operating system:

* egypt: To install follow instruction from http://www.gson.org/egypt/ or follow instructions in Installation section
* graphviz: `sudo apt-get install graphviz`
* python `sudo apt-get install python`

## Egypt
```
tar egypt-1.10.tar.gz
cd egypt-1.10
perl Makefile.PL
make
make install
```
## Callgr
To install __CallGr__ onto your system:

```
git clone https://github.com/leonoyd/callgr.git
cd callgr
python setup.py install
```

# Usage

__Running for the first time__

1.  navigate to the project directory
2.  run `make clean`
3.  run `make CFLAGS=-fdump-rtl-expand` or its equivalent, if running in an ide you need to
    add the flag to the compiler argument in options then rebuild the application. See note(1) below for more information
4.  run `callgr -u "function_name"`. The -u option tells the application to update its database (use this whenever you rebuild the appication)
5.  can also be invoked without a function name (ie `callgr -u`)

__Consecutive runs__

For consecutive runs simply remove the -u so that you dont regenerate the database file.

__Notes__

note(1): To get GCC to generate the files required RTL expand files, `-fdump-rtl-expand` needs to be added to the CFLAGS or CPPFLAGS
eg. `make CFLAGS=-fdump-rtl-expand` or `make CPPFLAGS=-fdump-rtl-expand`

note(2): The project directory needs to be in a location where all the object files are visible you won't
generate the proper structure.
