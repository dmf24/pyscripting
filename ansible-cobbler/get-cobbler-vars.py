#!/bin/env python
import xmlrpclib
import yaml
import json
import sys
import ansible.inventory
import ansible.constants
import argparse
from tempfile import SpooledTemporaryFile
import csv

cobbler_api_url='https://cobbler/cobbler_api'

def output_yaml(pydata):
    return yaml.dump(pydata, default_flow_style=False)

def output_json(pydata):
    return json.dumps(pydata, indent=2)

def output_csv(showheader=True):
    def csv_fn(pydata):
        csvfile=SpooledTemporaryFile()
        csvw=csv.writer(csvfile)
        fieldnames=[]
        for h in pydata:
            for k in pydata[h]:
                if k not in fieldnames:
                    fieldnames.append(k)
        if showheader:
            csvw.writerow(['system_name'] + fieldnames)
        for system_name in pydata:
            csvw.writerow([system_name] + [pydata[system_name].get(k, None) for k in fieldnames])
        csvfile.seek(0)
        results=csvfile.read()
        csvfile.close()
        return results
    return csv_fn

def md_table_row(lst):
    return "| %s |" % ' | '.join(lst)

def output_markdown(pydata):
    fieldnames=[]
    lines=[]
    for h in pydata:
        for k in pydata[h]:
            if k not in fieldnames:
                fieldnames.append(k)
    fieldnames.sort()
    lines.append(md_table_row(['system'] + fieldnames))
    lines.append(md_table_row(['---'] * len(['system'] + fieldnames)))
    for system_name in pydata:
        lines.append(md_table_row([system_name] + ["%s" % pydata[system_name].get(k, None) for k in fieldnames]))
    return '\n'.join(lines)
                    

helptext = '''usage: %s [options] host_pattern [[variable1] variable2...]
''' % sys.argv[0]

parser = argparse.ArgumentParser(description=helptext)

parser.add_argument('-l', '--limit', default=ansible.constants.DEFAULT_SUBSET, dest='subset',
                    help='further limit selected hosts to an additional pattern')

parser.add_argument('-j', '--json', action='store_true', help='Output json (default is yaml)')

parser.add_argument('-s', '--server', type=str, default=cobbler_api_url, help='Cobbler api url (default: %s)' % cobbler_api_url)

parser.add_argument('-c', '--csv', action='store_true', help='Output csv (default is yaml)')
parser.add_argument('--csv-with-header', action='store_true', dest='csvh', help='Output csv (default is yaml)')
parser.add_argument('--markdown', action='store_true', help='Output markdown (default is yaml)')
parser.add_argument('pattern', type=str, action='store', help="ansible inventory host pattern")

parser.add_argument('variables', type=str, nargs=argparse.REMAINDER, action='store', help="list of cobbler variables")

args=parser.parse_args()

if args.json:
    output=output_json
elif args.csv:
    output=output_csv(showheader=False)
elif args.csvh:
    output=output_csv(showheader=True)
elif args.markdown:
    output=output_markdown
else:
    output=output_yaml

inventory_manager = ansible.inventory.Inventory()
if args.subset:
    inventory_manager.subset(args.subset)
hosts = inventory_manager.list_hosts(args.pattern)

if len(hosts) == 0:
    callbacks.display("No hosts matched")
    sys.exit(0)

server=xmlrpclib.Server(args.server)

results={}

for system_name in hosts:
    data=server.get_system_as_rendered(system_name)
    if len(args.variables) == 0:
        results.setdefault(system_name, data)
    else:
        results.setdefault(system_name, {})
        for v in args.variables:
            if v in data.keys():
                results[system_name].setdefault(v, data[v])

print output(results)

