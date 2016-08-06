from process import process

def dumplist():
    results=process('sysctl -a')
    return [[y.strip() for y in x.split('=')] for x in results[1].split('\n') if x.strip() != '']

def dumpdict():
    return dict(dumplist())
