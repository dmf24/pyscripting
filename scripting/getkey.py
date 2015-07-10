
## http://python4fun.blogspot.com/2008/06/get-key-press-in-python.html
#############
######
import os
if os.name == 'posix':
    import termios, sys
    TERMIOS = termios
    def getkey():
        """For linux"""
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
        new[6][TERMIOS.VMIN] = 1
        new[6][TERMIOS.VTIME] = 0
        termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
        c = None
        try:
            c = os.read(fd, 1)
        finally:
            termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
        return c
#############
elif os.name == 'nt':
    import msvcrt

#### windows only ####
#http://stackoverflow.com/a/15313849/130432

    def readch(echo=True):
        "Get a single character on Windows."
        while msvcrt.kbhit():  # clear out keyboard buffer
            msvcrt.getwch()
        ch = msvcrt.getwch()
        if ch in u'\x00\xe0':  # arrow or function key prefix?
            ch = msvcrt.getwch()  # second call returns the actual key code
        if echo:
            msvcrt.putwch(ch)
        return ch
    
    def pause(prompt='Press any key to continue . . .'):
        if prompt:
            print prompt,
        readch(echo=False)
    getkey=readch

if __name__ == '__main__':
    ch=''
    while ch not in ['q', 'Q']:
        ch=getkey()
        print ch, ord(ch)
