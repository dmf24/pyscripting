from scripting import process
from scripting.quickmenu import getchoice
import sys
pri=sys.stdout.write
err=sys.stderr.write

up=list('qwertyuiop')
down=list('asdfghjklzxcvbnm,.')

def barename(txt):
    if txt.startswith('* '):
        return txt[2:]
    else:
        return txt

def switchbranch():
    gbresults=process('git branch')
    brlist=[x.strip() for x in gbresults[1].split('\n') if x.strip() != ''] + ['NONE']
    choice=getchoice(brlist, up=up, down=down)
    
    if choice != 'NONE':
        results=process("git checkout %s" % barename(choice))
        pri(results[1])
        err(results[2]) if len(results[2].strip()) > 0 else None
    else:
        return 0
    return results[0]

if __name__=='__main__':
    sys.exit(switchbranch())

