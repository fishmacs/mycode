import re
import string
import struct

class Invalid(Exception): pass
class Impossible(Exception): pass

class Puzzle:
    ASCII = '.123456789'
    BIN = '\0\1\2\3\4\5\6\7\10\11'

    def __init__(self, lines):
        if type(lines) is list:
            s = '\n'.join(lines)
        else:
            s = lines
        s = s.strip()
        if len(s) != 81:
            raise Invalid('Grid is the wrong size')

        m = re.search(r'[^12345678\.]', s)
        if m:
            raise Invalid('Illegal character %s in puzzle' % s[m.start()])

        s = s.translate(string.maketrans(self.ASCII, self.BIN))
        self.grid = list(struct.unpack('81B', s))
        if self.has_duplicates():
            raise Invalid("Initial puzzle has duplicates")

    def __str__(self):
        
    