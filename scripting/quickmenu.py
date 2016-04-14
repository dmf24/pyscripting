from getkey import getkey

clsstr=chr(27) + '[2J'

def pfn_cursor(astring, menunum=''):
    return "> %s" % astring

def pfn(astring, menunum):
    return "  %s" % astring

def lstmenu(lst, cursor, pfn_cursor=pfn_cursor, pfn=pfn):
    print clsstr + '\n'.join([pfn_cursor(u, n) if cursor==n else pfn(u,n)
                              for n, u in zip(range(len(lst)), lst)])

def threemenu(lst, cursor, disabled_list, finished_list, pfn_cursor=pfn_cursor, pfn=pfn):
    lst=[pfn_cursor(u, n) if cursor==n else pfn(u,n)
         for n, u in zip(range(len(lst)), lst)]
    print clsstr + '\n'.join(['+[%s]' % x if x in finished_list else '--%s' % x for x in finished_list + disabled_list]) + '\n\n' + '\n'.join(lst)

def getchoice3(lst, disabled_list, finished_list,
              up=['w', 'i'],
              down=['s', 'k'],
              enter=['\n'],
              escape=[chr(27)],
              menu_fn=threemenu,
              cursor=0):
    ch=''
    menu_fn(lst, cursor, disabled_list, finished_list)
    while ch not in escape:
        if ch in down:
            cursor = (cursor + 1) % len(lst)
        elif ch in up:
            cursor = (cursor - 1) % len(lst)
        elif ch in enter:
            return lst[cursor]
        elif ch in escape:
            return None
        menu_fn(lst, cursor, disabled_list, finished_list)
        ch=getkey()
    return None

def getchoice(lst,
              up=['w', 'i'],
              down=['s', 'k'],
              enter=['\n'],
              escape=[chr(27)],
              menu_fn=lstmenu,
              cursor=0):
    ch=''
    menu_fn(lst, cursor)
    while ch not in escape:
        if ch in down:
            cursor = (cursor + 1) % len(lst)
        elif ch in up:
            cursor = (cursor - 1) % len(lst)
        elif ch in enter:
            return lst[cursor]
        elif ch in escape:
            return None
        menu_fn(lst, cursor)
        ch=getkey()
    return None
