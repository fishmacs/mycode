#encoding=utf8

import codecs
import xlrd


def load_gou():
    wb = xlrd.open_workbook('/Users/zw/Downloads/狗.xlsx')
    sheet = wb.sheets()[0]
    ret = {}
    for i in xrange(1, sheet.nrows - 1):
        row = sheet.row_values(i)
        types = sheet.row_types(i)
        if types[0] == 1:
            name = row[0]
        else:
            try:
                name = str(int(row[0]))
            except:
                name = u'150元套组'
        ret[name] = (row[2], row[4])
    return ret


def total(d):
    x = y = 0
    for n, (v1, v2) in d.iteritems():
        x += v1
        y += v2
    return x, y


def total1(d):
    f = lambda (u, v), (_, (x, y)): (u + x, v + y)
    return reduce(f, d.iteritems(), (0, 0))


def load_gou2(p):
    wb = xlrd.open_workbook('/Users/zw/Downloads/员工特卖订单 2016Q4.xlsx')
    sheet = wb.sheets()[0]
    ret = {}
    for i in xrange(4, sheet.nrows - 2):
        row = sheet.row_values(i)
        if row[p]:
            types = sheet.row_types(i)
            if types[0] == 1:
                name = row[0]
            else:
                name = str(int(row[0]))
            if types[4] == 0:
                price = 150
            else:
                price = row[4]
            num = int(row[p])
            ret[name] = (num, price * num)
    return ret


def extract(filename, outfile):
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheets()[0]
    with codecs.open(outfile, 'wb', 'gbk') as f:
        lines = []
        for i in xrange(4, sheet.nrows - 2):
            row = [unicode(x) for x in sheet.row_values(i)]
            if row[1]:
                line = ','.join([row[0], row[1][6:], row[3], row[4], row[5], row[6], row[2]])
                lines.append(line)

        lines = sorted(lines, key=lambda line: str(line[0]))
        for line in lines:
            f.write(line + '\n')
