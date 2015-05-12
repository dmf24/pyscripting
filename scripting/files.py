#
# This is a library for miscellanous support functions used by
# python scripts in the HMS chef deployment.
#

import sys, os
from tempfile import SpooledTemporaryFile
import string
import ConfigParser
import pwd, grp

__all__=['appendlist2file', 'chunks', 'dirs_and_files', 'file2list', 'fileownership', 'finddirs', 'findfiles', 'list2file', 'listconfig', 'os', 'pwd', 'readconfig', 'readconfig2dict', 'string', 'string2spool', 'stripfile2list']

# misc

def chunks(lst, n):
    'split a list into size n chunks'
    return [lst[i:i+n] for i in range(0, len(lst), n)]

#
# Common file functions
#

# These functions are convenient for smaller files
# where memory is not a concern.

# file(filename).readlines() is more portable
def file2list(filename):
    """file2list(filename)
    Reads a file into a list and returns it.
    >>> isinstance(file2list(os.path.abspath(sys.argv[0])), list)
    True
    """
    FILE = open(filename, "r")
    x=FILE.readlines()
    FILE.close()
    return x

def list2file(filename, lst, rwabit='w'):
    """list2file(filename, lst, rwabit='w')
    Writes each item of lst to a line in a file specified by filename"""
    FILE = open(filename, rwabit)
    FILE.writelines(lst)
    FILE.close()

def stripfile2list(filename):
    """Reads an entire file into a list and strips"""
    return [x.strip() for x in file2list(filename)]

def appendlist2file(filename, lst):
    """Appends lst to file specified by filename """
    list2file(filename, lst, rwabit='a')

def string2spool(input_string):
    """Takes a string as an argument and returns an open file handle with the
    contents of the string"""
    file_object=SpooledTemporaryFile()
    file_object.write(input_string)
    file_object.seek(0)
    return file_object

#
# ConfigParser wrappers
#


def readconfig(filename, magic=False):
    """Parse a config file and return a parsing object"""
    if magic:
        parser=ConfigParser.SafeConfigParser()
    else:
        parser=ConfigParser.RawConfigParser()
    #enable case-sensitivity
    parser.optionxform=str
    parser.read(filename)
    return parser

def listconfig(parser_object):
    """Return a list with all of the data from a configfile parser object"""
    return [(x, parser_object.items(x)) for x in parser_object.sections()]

def readconfig2dict(filename):
    return dict(listconfig(readconfig(filename)))

#
#  filesystem wrappers
#


def findfiles(rootdir):
    for root, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            yield os.path.join(root, filename)

def finddirs(rootdir):
    for root, dirnames, filenames in os.walk(rootdir):
        for dirname in dirnames:
            yield os.path.join(root, dirname)

def dirs_and_files(rootdir):
    dl=[]
    fl=[]
    for root, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            fl.append(os.path.join(root, filename))
        for dirname in dirnames:
            dl.append(os.path.join(root, dirname))
    return (dl, fl)

def fileownership(filename, convert=True):
    """Return a tuple containing the (owner, group) for a path.
    Set convert=False to return (uid, gid) instead."""
    filestat=os.stat(filename)
    if convert is False:
        return (filestat.st_uid, filestat.st_gid)
    else:
        return (uid2name(filestat.st_uid), groupname(filestat.st_gid))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
