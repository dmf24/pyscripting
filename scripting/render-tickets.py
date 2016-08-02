#!/home/dmf24/virtual-environments/pyscripting-2.7.10/bin/python
import json
import os
import sys

datadir=sys.argv[1]

ticketdata={}
for ticket in os.listdir(datadir):
    ticketdata.setdefault(ticket, json.loads(file(os.path.join(datadir, ticket)).read()))

ticket_template='''<br><a href="{url}">{id}</a>: {text}'''
comment_template='''{user}({tm}): {txt}'''

def render_commentary(commentary_list):
    if len(commentary_list) != 1:
        lst=[]
        for user, tm, txt in commentary_list:
            lst.append(comment_template.format(user=user, tm=tm, txt=txt))
        return '\n'.join(['<ul>'] + ['  <li>%s</li>\n' % x for x in lst] + ['</ul>'])
    else:
        user, tm, txt = commentary_list[0]
        return comment_template.format(user=user, tm=tm, txt=txt)

for ticket, data in ticketdata.items():
    print ticket_template.format(text=render_commentary(data['commentary']), **data)
