# CallGr

Generates a call graph from information obtain from GCC compilation process

CallGr is intended to give its user a high level/birds eye view of the entire codebase or a subsection

The program is not a self contained program. It works by calling two other programs, both of which needs to presented on your 
operating system in order to use this application.

# Installation

# Pre-requisites
Considering ubuntu operating system

* egypt: To install follow instruction from http://www.gson.org/egypt/ 
* graphvixz: sudo apt-get install graphviz
* python sudo apt-get install python

To install __CallGr__ onto your system:

```
git clone https://github.com/leonoyd/callgr.git
cd callgr
python setup.py install
```

# Usage

__Running for the first time__

* navigate to the project directory
* run `make clean`
* run `make CFLAGS=-fdump-rtl-expand` or its equivalent, if running in an ide you need to 
  add the flag to the compiler argument in options then rebuild the application. See note(1) below for more information
* run `./callgr -u "function_name"`
  -u option tells the application to update its database(use this whenever you rebuild the appication)
* can also be involed without a function name ie ./callgr -u

__Consecutive runs__

For consecutive runs simply remove the -u so that you dont regenerate the database file.

__Notes__
note(1): To get GCC to generate the files required(rtl.expand) the -fdump-rtl-expand need to be appended to the CFLAGS or CPPFLAGS
eg. `make CFLAGS=-fdump-rtl-expand` or `make CPPFLAGS=-fdump-rtl-expand`

note(2): The project directory needs to be in a location where all the object files are visible you won't 
generate the proper structure.


