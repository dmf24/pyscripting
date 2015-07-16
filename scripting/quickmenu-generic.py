from scripting import process
from scripting.quickmenu import getchoice
from scripting import stripfile2list, list2file
import sys, os
pri=sys.stdout.write
err=sys.stderr.write

def nullout(*args):
    return None

debug=nullout

menudir=os.path.join(os.getenv('HOME'), '.quickmenu')

if not os.path.exists(menudir):
    os.makedirs(menudir)

up=list('qwertyuiop')
down=list('asdfghjklzxcvbnm,.')

optionsfile=os.path.join(menudir, '%s.options' % sys.argv[1])
nonefile=os.path.join(menudir, '%s.nonevalue' % sys.argv[1])
nextfile=os.path.join(menudir, '%s.next' % sys.argv[1])

if os.path.isfile(optionsfile):
    debug("loading %s" % optionsfile)
    options=[x.strip() for x in file(optionsfile).readlines() if x != '']
else:
    err("%s does not exist, waiting for menu options on stdin" % optionsfile)
    options=[x.strip() for x in sys.stdin.readlines() if x != '']

if os.path.isfile(nonefile):
    nonevalue=stripfile2list(nonefile)[0]
else:
    nonevalue=False

def chooser():
    if nonevalue is not False:
        choices=options + [nonevalue]
    else:
        choices=options
    choice=getchoice(choices, up=up, down=down)
    if choice != nonevalue:
        list2file(nextfile, [choice])
        debug("Set %s to %s" % (choice, nextfile))
    return 0

if __name__=='__main__':
    sys.exit(chooser())
