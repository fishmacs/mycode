#encoding=utf8

import os
import codecs
import xlrd

head_rows = 3
tail_rows = 2
code_col = 1
name_col = 2
price_col = 4
amount_col = 6
final_txt = '特卖.txt'
final_csv = '特卖.csv'
deliver = 'deliver.txt'


def product_code(row, types, code_col):
    if types[code_col] == 1:
        return row[code_col]
    else:
        return str(int(row[code_col]))


def load_all(filename):
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheets()[0]
    ret = {}
    codes = []
    for i in xrange(head_rows, sheet.nrows - tail_rows):
        row = sheet.row_values(i)
        code = product_code(row, sheet.row_types(i), code_col)
        codes.append(code)
        ret[code] = (row[name_col], row[price_col])
    return ret


def process_txt(filename, all_items):
    ret = {}
    with open(filename) as f:
        lines = f.read()
        peoples = lines.split('\n\n')
        for people in peoples:
            lines = people.split('\n')
            if lines[0]:
                ret[lines[0]] = d = {}
                for line in lines[1:]:
                    fields = line.split()
                    if len(fields) > 1:
                        d[fields[0].upper()] = int(fields[1])
    print_result(ret, all_items)
    # save_csv(ret, final_csv, all_items)
    save_deliver(ret, deliver)
    return ret


def save_deliver(orders, filename):
    ret = {}
    for name, order in orders.iteritems():
        for code, amount in order.iteritems():
            ret.setdefault(code, {})
            ret[code].setdefault(name, 0)
            ret[code][name] += amount
    codes = sorted(ret.keys())
    with open(filename, 'w') as f:
        for code in codes:
            f.write(code + ':\t')
            buyers = ret[code]
            for buyer, amount in buyers.iteritems():
                if amount:
                    f.write('%s, %d ' % (buyer, amount))
            f.write('\n\n')


def save_csv(orders, filename, all_items):
    ret = {}
    for name, order in orders.iteritems():
        for code, amount in order.iteritems():
            ret.setdefault(code, 0)
            ret[code] += amount
    with codecs.open(filename, 'wb', 'gbk') as f:
        codes = sorted(ret.keys())
        n = 0
        total_price = 0
        for code in codes:
            amount = ret[code]
            name = all_items[code][0]
            price = all_items[code][1] * amount
            f.write('%s, %s, %d, %.2f\n' % (code, name, amount, price))
            n += amount
            total_price += price
        print n, total_price


def print_result(ret, all_items):
    for name, order in ret.iteritems():
        price = 0
        n = 0
        for code, amount in order.iteritems():
            #print code, amount, all_items[code][1]
            price += amount * all_items[code][1]
            n += amount
        print '%s: %d, %f' % (name, n, price)

    #with codecs.open(outfile, 'wb', 'utf-8') as f:
    #with open(outfile, 'w') as f:


def process(filename):
    name = os.path.splitext(os.path.basename(filename))[0]
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheets()[0]
    ret = {}
    for i in xrange(head_rows, sheet.nrows - tail_rows):
        row = sheet.row_values(i)
        code = product_code(row, sheet.row_types(i), code_col)
        amount = row[amount_col]
        if amount:
            ret[code] = int(amount)
    append_txt(name, ret, final_txt)


def append_txt(name, order, filename):
    with open(filename, 'a') as f:
        f.write(name + '\n')
        codes = sorted(order.keys())
        for code in codes:
            f.write('%s %d\n' % (code, order[code]))
        f.write('\n')


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


if __name__ == '__main__':
    import sys
    base_dir = sys.argv[1]
    global final_txt, final_csv, deliver
    final_txt = os.path.join(base_dir, final_txt)
    final_csv = os.path.join(base_dir, final_csv)
    deliver = os.path.join(base_dir, deliver)

    all_items = load_all(os.path.join(base_dir, sys.argv[2] + '.xlsx'))
    for xlsx in sys.argv[3:]:
        process(os.path.join(base_dir, xlsx + '.xlsx'))
        process(os.path.join(base_dir, xlsx + '.xlsx'))
    orders = process_txt(final_txt, all_items)
    save_csv(orders, final_csv, all_items)
