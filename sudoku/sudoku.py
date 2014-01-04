import re
import string
import struct
import copy


class Invalid(Exception):
    pass


class Impossible(Exception):
    pass


class Puzzle:
    ASCII = '.123456789'
    BIN = '\0\1\2\3\4\5\6\7\10\11'
    BOX_OF_INDEX = [0, 0, 0, 1, 1, 1, 2, 2, 2,
                    0, 0, 0, 1, 1, 1, 2, 2, 2,
                    0, 0, 0, 1, 1, 1, 2, 2, 2,
                    3, 3, 3, 4, 4, 4, 5, 5, 5,
                    3, 3, 3, 4, 4, 4, 5, 5, 5,
                    3, 3, 3, 4, 4, 4, 5, 5, 5,
                    6, 6, 6, 7, 7, 7, 8, 8, 8,
                    6, 6, 6, 7, 7, 7, 8, 8, 8,
                    6, 6, 6, 7, 7, 7, 8, 8, 8]
    BOX_TO_INDEX = [0, 3, 6, 27, 30, 33, 54, 57, 60]
    ALL_DIGITS = set(xrange(1, 10))

    def __init__(self, lines):
        if type(lines) is list:
            s = ''.join(lines)
        else:
            s = lines
        s = re.sub('\s+', '', s)
        if len(s) != 81:
            raise Invalid('Grid is the wrong size')

        m = re.search(r'[^123456789\.]', s)
        if m:
            raise Invalid('Illegal character %s in puzzle' % s[m.start()])

        s = s.translate(string.maketrans(self.ASCII, self.BIN))
        self.grid = list(struct.unpack('81B', s))
        if self.has_duplicates():
            raise Invalid("Initial puzzle has duplicates")

    def __str__(self):
        translator = string.maketrans(self.BIN, self.ASCII)
        rows = [struct.pack('9B', *self.grid[r*9:r*9+9]) for r in xrange(9)]
        return '\n'.join(rows).translate(translator)

    def __getitem__(self, (row, col)):
        return self.grid[row*9 + col]

    def __setitem__(self, (row, col), val):
        if val not in range(10):
            raise Invalid('Illegal cell value')
        self.grid[row*9 + col] = val

    def copy(self):
        return copy.deepcopy(self)

    def get_unknown(self):
        for i in xrange(81):
            if self.grid[i] == 0:
                row = i / 9
                col = i % 9
                yield row, col, self.BOX_OF_INDEX[i]

    def has_duplicates(self):
        all(len(set(x)) == len(x) for i in xrange(9) for x in
            (self.row_digits(i), self.col_digits(i), self.box_digits(i)))

    def possible(self, row, col, box):
        return self.ALL_DIGITS.difference(
            set(self.row_digits(row)).union(
                set(self.col_digits(col)).union(
                    set(self.box_digits(box)))))

    def row_digits(self, row):
        return filter(lambda x: x > 0, self.grid[row*9:row*9+9])

    def col_digits(self, col):
        return filter(lambda x: x > 0, [self.grid[i] for i in
                                        xrange(col, 81, 9)])

    def box_digits(self, box):
        i = self.BOX_TO_INDEX[box]
        return filter(lambda x: x > 0,
                      [self.grid[x+y] for x in xrange(i, i + 19, 9)
                       for y in xrange(3)])


def scan(puzzle):
    changed = True
    while changed:
        changed = False
        rmin, cmin, pmin = [None] * 3
        min = 10
        for row, col, box in puzzle.get_unknown():
            p = puzzle.possible(row, col, box)
            if not p:
                raise Impossible
            elif len(p) == 1:
                puzzle[row, col] = p.pop()
                changed = True
            else:
                if not changed and len(p) < min:
                    min = len(p)
                    rmin, cmin, pmin = row, col, p
    return rmin, cmin, pmin


def solve(puzzle):
    puzzle = puzzle.copy()
    r, c, p = scan(puzzle)
    if not r:
        return puzzle

    for guess in p:
        puzzle[r, c] = guess
        try:
            return solve(puzzle)
        except Impossible:
            pass

    raise Impossible()
