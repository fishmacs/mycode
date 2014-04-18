import unittest
from unittest import TestCase

from attr import AttrDict4 as AttrDict


class AttrDictTest(TestCase):
    def test_simple(self):
        d = AttrDict()
        d.abc = 1
        self.assertEqual(d.abc, 1)
        self.assertEqual(d['abc'], 1)
        self.assertEqual(len(d), 1)
        del(d.abc)
        self.assertRaises(AttributeError, lambda: d.abc)
        d.count = 0
        self.assertEqual(d.count, 0)
        del(d['count'])
        self.assertRaises(AttributeError, lambda: d.count)
        self.assertEqual(len(d), 0)

    def test_default_value(self):
        d = AttrDict(defval='', attrerr=False)
        d1 = AttrDict(defval=0, attrerr=False)
        self.assertEqual(d.a, '')
        self.assertEqual(d1.a, 0)
        
    def test_kargs(self):
        d = AttrDict(a=1, b=2, c=3)
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 2)
        self.assertEqual(d.c, 3)

if __name__ == '__main__':
    unittest.main()
