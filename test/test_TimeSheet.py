#!/usr/bin/python

import os,sys,csv
cmd_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import unittest,TimeSheet

mock_csvContent = [
    ['2011-01-01', '01h00', '00h01'],
    ['2011-01-02', '02h00', '00h02'],
    ['2011-01-03', '03h00', '00h03'],
]

class mock_file():
    def open(self, name):
        pass

    def seek(self, n):
        pass

    def read(self, n):
        return 'date\tAM\tPM' + '\n'

class mock_csv():
    def open(self, name):
        pass

    def seek(self, n):
        pass
    
    def next(self):
        return ['date', 'AM', 'PM']

def mock_setCsvSource(obj, a, b):
    obj.csv = mock_file()
    obj.csvReader = mock_csv()

setattr(TimeSheet.TimeSheet, 'setCsvSource', mock_setCsvSource)

class testCounter(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        # csv.reader = mock_reader
        # csv.Sniffer.has_header = mock_has_header
        self.timesheet = TimeSheet.TimeSheet('test counter', [0])
        self.timesheet.csvReader = mock_csvContent
    
    def test_setNumericGroups(self):
        self.timesheet.setGroups('1,2,1+2')
        for c in self.timesheet._counters:
            self.assertIsInstance(c, TimeSheet.Counter)
        self.assertEqual(len(self.timesheet._counters), 1 + 3)
        self.assertEqual(self.timesheet._counters[1]._hits, [1])
        self.assertEqual(self.timesheet._counters[1].name, '1')
        self.assertEqual(self.timesheet._counters[2]._hits, [2])
        self.assertEqual(self.timesheet._counters[2].name, '2')
        self.assertEqual(self.timesheet._counters[3]._hits, [1, 2])
        self.assertEqual(self.timesheet._counters[3].name, '1+2')
    
    def test_setLabelGroups(self):
        self.timesheet.setGroups('AM,PM,AM+PM')
        for c in self.timesheet._counters:
            self.assertIsInstance(c, TimeSheet.Counter)
        self.assertEqual(len(self.timesheet._counters), 1 + 3)
        self.assertEqual(self.timesheet._counters[1]._hits, [1])
        self.assertEqual(self.timesheet._counters[1].name, 'AM')
        self.assertEqual(self.timesheet._counters[2]._hits, [2])
        self.assertEqual(self.timesheet._counters[2].name, 'PM')
        self.assertEqual(self.timesheet._counters[3]._hits, [1, 2])
        self.assertEqual(self.timesheet._counters[3].name, 'AM+PM')

    def test_header(self):
        self.assertEqual(self.timesheet._header, ['date', 'AM', 'PM'])

    def test_resetBounds(self):
        self.assertEqual(len(self.timesheet.bounds), 2)
        self.assertEqual(set(self.timesheet.bounds.keys()), set(['lower', 'upper']))

    def test_sumBetween(self):
        self.timesheet.sumBetween('2011-01-01', '2011-01-01')
        self.assertEqual(self.timesheet._counters[0]._sum, 61)

    def test_sumAfter(self):
        self.timesheet.sumAfter('2011-01-02')
        self.assertEqual(self.timesheet._counters[0]._sum, 5*60+5)

    def test_sumBefore(self):
        self.timesheet.sumBefore('2011-01-02')
        self.assertEqual(self.timesheet._counters[0]._sum, 3*60+3)

    def test_sum(self):
        self.timesheet.sum()
        self.assertEqual(self.timesheet._counters[0]._sum, 6*60+6)

        

if __name__ == '__main__':
    unittest.main()