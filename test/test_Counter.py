#!/usr/bin/python

import os,sys
cmd_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import unittest,TimeSheet

class testCounter(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.counter = TimeSheet.Counter('test counter', [0])
    
    def test_days(self):
        self.assertEqual(self.counter.days(), (0, 0, 0))
        self.counter._sum = 42
        self.assertEqual(self.counter.days(), (0, 0, 42))
        self.counter._sum = 60
        self.assertEqual(self.counter.days(), (0, 1, 0))
        self.counter._sum = 102
        self.assertEqual(self.counter.days(), (0, 1, 42))
        self.counter._sum = 456
        self.assertEqual(self.counter.days(), (1, 0, 0))
        self.counter._sum = 457
        self.assertEqual(self.counter.days(), (1, 0, 1))
        self.counter._sum = 517
        self.assertEqual(self.counter.days(), (1, 1, 1))
        
    def test_feed(self):
        self.assertEqual(self.counter._sum, 0, 'wrong initial sum value')
        self.counter.feed(['0h01'])
        self.assertEqual(self.counter._sum, 1, 'feeding the counter went bad')
        self.counter.feed(['0h01', '0h01'])
        self.assertEqual(self.counter._sum, 2, 'feeding the counter went bad')
    
    def test_getSum(self):
        self.assertEqual(self.counter.getSum(), 0, 'getting sum failed')
        self.counter.feed(['0h05'])
        self.assertEqual(self.counter.getSum(), 5, 'getting sum failed')

    def test_hours(self):
        self.assertEqual(self.counter.hours(), (0, 0))
        self.counter._sum = 42
        self.assertEqual(self.counter.hours(), (0, 42))
        self.counter._sum = 60
        self.assertEqual(self.counter.hours(), (1, 0))
        self.counter._sum = 102
        self.assertEqual(self.counter.hours(), (1, 42))
        
    def test_reset(self):
        self.counter.reset()
        self.assertEqual(self.counter._sum, 0, 'resetting counter to default value failed')
        self.counter.reset(100)
        self.assertEqual(self.counter._sum, 100, 'resetting counter to a custom value failed')

    def test_str(self):
        self.assertIsInstance(self.counter.__str__(), str)
      
    def test_toMinutes(self):
        self.assertEqual(self.counter._toMinutes('02h02'), 122, 'converting string to minutes failed')
        self.assertEqual(self.counter._toMinutes('00h02'), 2, 'converting string to minutes failed')
        

if __name__ == '__main__':
    unittest.main()