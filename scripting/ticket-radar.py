#!/home/dmf24/virtual-environments/pyscripting-2.7.10/bin/python
import yaml
import json
from urllib import urlencode
from scripting import stripfile2list, list2file
import sys, os
pri=sys.stdout.write
err=sys.stderr.write
import argparse
import copy
from datetime import datetime
today=datetime.today

def nullout(*args):
    return None

debug=nullout

jp=os.path.join

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

def istoken(strng):
    if len(strng.split()) == 1:
        return True
    else:
        return False

def extract_tickets(lst_or_string, tickets=[]):
    tickets=set()
    if isinstance(lst_or_string, list):
        for itm in lst_or_string:
            tickets.update(extract_stat(itm))
    return tickets

def parse_tickets(lst):
    tickets=[x.strip() for x in lst if isstat(x.strip())]
    return [tickets, ' '.join(lst)]

defaults = {
    'config' : jp(os.getenv('HOME'), '.ticket-radar/config'),
    'datadir' : jp(os.getenv('HOME'), '.ticket-radar/data'),
    'user' : os.getenv('USER')
    }

config=copy.deepcopy(defaults)
config.setdefault('current-user', os.getenv('USER'))

parser=argparse.ArgumentParser(description="ticket alert system")
paa=parser.add_argument

for key in defaults.keys():
    paa('-%s' % key[0], '--%s' % key, metavar=key, default=config[key], help="default: %s" % config[key])

paa('newticket', type=str, nargs='+', help="<comment with ticket number>")

args=parser.parse_args()

for key in defaults.keys():
    if key in args.__dict__.keys():
        config.setdefault(key, args.__dict__[key])

def newticket(ticket, commentary):
    new_ticket={}
    new_ticket.setdefault('id', ticket)
    new_ticket.setdefault('commentary', [comment_entry(commentary)])
    if isstat(ticket):
        new_ticket.setdefault('url', staturl(ticket))
    return new_ticket

def is_commentary_present(ticketstruct, commentary):
    for commenter, commenttime, comment in ticketstruct['commentary']:
        if comment == commentary:
            return True
    return False

def comment_entry(commentary):
    return [config['current-user'], '%s' % today(), commentary]

if not os.path.isdir(config['datadir']):
    err('Error: data directory does not appear to exist: %s\n' % config['datadir'])
    err('please create before using this script\n')
    sys.exit(1)

userdata=jp(config['datadir'], config['user'])

stat=jp(userdata, 'stat')

if not os.path.isdir(userdata):
    os.mkdir(userdata)
if not os.path.isdir(stat):
    os.mkdir(stat)

def write_tickets(ticketdata):
    parentdir=jp(config['datadir'], config['user'])
    for tdir in ticketdata.keys():
        for ticket in ticketdata[tdir]:
            with open("%s" % jp(jp(parentdir, tdir), ticket), 'w') as tf:
                tf.write(json.dumps(ticketdata[tdir][ticket]))

def write_ticket(ttype, tstruct):
    ticket=tstruct['id']
    parentdir=jp(config['datadir'], config['user'])
    with open("%s" % jp(jp(parentdir, ttype), ticket), 'w') as tf:
        tf.write(json.dumps(tstruct))

def load_ticket(t):
    if isstat(t):
        return json.loads(file(jp(stat, t)).read())

ticketdata={   
    'stat': dict([(t, load_ticket(t)) for t in os.listdir(stat)])
    }

#if os.path.isfile(configfile):
#    debug("loading %s" % optionsfile)
#    config=yaml.load(file(configfile))


commentary=' '.join(args.newticket)
tickets=list(extract_tickets(args.newticket))

for ticket in tickets:
    if ticket in ticketdata['stat'].keys():
        if not is_commentary_present(ticketdata['stat'][ticket], commentary):
            ticketdata['stat'][ticket]['commentary'].append(comment_entry(commentary))
            write_ticket('stat', ticketdata['stat'][ticket])
    else:
        ticketdata['stat'].setdefault(ticket, newticket(ticket, commentary))
        write_ticket('stat', ticketdata['stat'][ticket])
