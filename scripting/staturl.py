#!/usr/bin/env python

from urllib import urlencode

def isstat(tstring):
    if tstring.startswith('inc') or tstring.startswith('INC'):
        if tstring[3:10].isdigit():
            return True
    return False


def staturl(tstring):
    params=urlencode(dict(sysparm_tsgroups='',
                          sysparm_view='text_search',
                          sysparm_search=tstring))
    return 'https://harvardmed.service-now.com/textsearch.do?%s' % params

if __name__ == '__main__':
    import sys
    for x in sys.argv[1:]:
        print staturl(x)
