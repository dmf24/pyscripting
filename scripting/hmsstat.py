#!/usr/bin/env python

from urllib import urlencode
import logging

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

def extract_stat(strng):
    candidates=set([])
    for prefix in ['inc', 'INC']:
        if prefix in strng:
            tokens=strng.split(prefix)
            for toke in tokens[1:]:
                if toke[:7].isdigit():
                    candidates.add('INC%s' % toke[:7])
    return candidates

def extract_tickets(lst_or_string, tickets=[]):
    tickets=set()
    if isinstance(lst_or_string, list):
        for itm in lst_or_string:
            tickets.update(extract_stat(itm))
    else:
        tickets.update(extract_stat(lst_or_string))
    return tickets

if __name__ == '__main__':
    import sys
    for x in sys.argv[1:]:
        print staturl(x)
