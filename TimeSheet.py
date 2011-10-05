#!/usr/bin/python

import csv,time,sys

class TimeSheet:
	'''Provides easy computation on timesheets. The sheet is a simple CSV file and 
	a CSV line should match this pattern : YYYY-MM-DD	HH:SS	HH:SS
	The 1st element is the date, the second is the amount of time spent in the morning
	and the last is the amount of time spent afternoon.
	
	Various functions are provided to compute the global sum and before, after or between dates.
	The sum can be expressed in hours and minutes or in days, hours and minutes.
	'''

	def __init__(self, csvSource, dialect="excel-tab"):
		self.csvSource = csvSource
		self.csv = open(self.csvSource, 'rb')
		self.csvReader = csv.reader(self.csv, dialect)
		self.resetBounds()
		self.resetSum()
	
	def resetBounds(self):
		'''Reset the bounds to sentinel values.'''
		self.bounds = {'lower': '1111-01-01', 'upper': '9999-01-01'}
	
	def resetSum(self, n=0):
		'''Reset the sum to a given value that defaults to 0.'''
		self._sum = n
		self.csv.seek(0)

	def sumBetween(self, lower, upper):
		'''Computes a new sum for timesheet entries between 2 given dates.'''
		self.resetSum()
		self.bounds['lower'] = lower
		self.bounds['upper'] = upper
		return self.sum()
	
	def sumAfter(self, lower):
		'''Computes a new sum for timesheet entries after a given date.'''
		self.resetBounds()
		self.resetSum()
		self.bounds['lower'] = lower
		return self.sum()

	def sumBefore(self, upper):
		'''Computes a new sum for timesheet entries before a given date.'''
		self.resetBounds()
		self.resetSum()
		self.bounds['upper'] = upper
		return self.sum()

	def sum(self):
		'''Computes the sum for timesheet entries between the instance date bounds.'''
		if self._sum:
			return _sum
		for line in self.csvReader:
			if self.bounds['lower'] <= line[0] and line[0] <= self.bounds['upper']:
				self._sum += self._toMinutes(line[1]) + self._toMinutes(line[2])
		return self
	
	def _duration(self, start, end):
		'''Computes the duration between 2 dates (that are in the same 24h interval), in minutes.'''
		start = start.split('h')
		end = end.split('h')
		if start[0] > end[0]:
			end[0] = int(end[0]) + 24
		return (int(end[0]) - int(start[0])) * 60 + int(end[1]) - int(start[1])
	
	def _toMinutes(self, hm):
		'''Converts a duration expressed as HH:MM in minutes.'''
		h, m = hm.split('h')
		return int(h) * 60 + int(m)
	
	def hours(self, mih=60):
		'''Returns a tuple containing the sum expressed as hours and minutes.'''
		signum = 1 if self._sum >= 0 else -1
		absSum = abs(self._sum)
		h = absSum / mih
		m = absSum % mih
		return (signum * h, signum * m)

	def days(self, mid=456, mih=60):
		'''Returns a tuple containing the sum expressed as days, hours and minutes.'''
		signum = 1 if self._sum >= 0 else -1
		absSum = abs(self._sum)
		d = absSum / mid
		left = absSum - d * mid
		left, self._sum = self._sum, left
		h, m = self.hours()
		self._sum, left = left, self._sum
		return (signum * d, signum * h, signum * m)


if __name__ == '__main__':
	args = sys.argv[1:]
	print args
	csvIn = args[0]
	ts = TimeSheet(csvIn)
	if len(args) == 1:
		ts.sum()
	elif len(args) == 3:
		getattr(ts, 'sum' + args[1].capitalize())(args[2])
	elif len(args) == 4:
		ts.sumBetween(args[2], args[3])
	print ts.hours()
	print ts.days()
