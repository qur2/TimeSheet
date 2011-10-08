#!/usr/bin/python

import csv,time,sys,getopt

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
		self._getHeaders()
		self._counters = [Counter('*', [1, 2])]
		self.resetBounds()
		self.resetSum()
	
	def setGroups(self, cols):
		colgroups = cols.split(',')
		for group in colgroups:
			hits = []
			for i in group.split('+'):
				try:
					hits += [int(i)]
				except ValueError:
					hits += [self._headers.index(i)]
			self._counters += [Counter(group, hits)]

	def _getHeaders(self):
		csvSample = self.csv.read(1024)
		self.csv.seek(0)
		hasHeader = csv.Sniffer().has_header(csvSample)
		self._headers = self.csvReader.next() if hasHeader else range(len(self.csvReader.next()))

	def resetBounds(self):
		'''Reset the bounds to sentinel values.'''
		self.bounds = {'lower': '1111-01-01', 'upper': '9999-01-01'}
	
	def resetSum(self, n=0):
		'''Reset the sum to a given value that defaults to 0 and rewind the file reader.'''
		for counter in self._counters:
			counter.reset(n)
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
		for line in self.csvReader:
			if self.bounds['lower'] <= line[0] and line[0] <= self.bounds['upper']:
				for counter in self._counters:
					counter.feed(line)
		return self

	def __str__(self):
		o = '';
		for c in self._counters:
			o += c.name + ' : ' + c.days().__str__() + '\n'
		return o


class Counter:
	def __init__(self, name, hits):
		self.name = name
		self._hits = hits
		self.reset()

	def feed(self, line):
		for hit in self._hits:
			self._sum += self._toMinutes(line[hit])
	
	def _toMinutes(self, hm):
		'''Converts a duration expressed as HHhMM in minutes.'''
		h, m = hm.split('h')
		return int(h) * 60 + int(m)
	
	# def _duration(self, start, end):
	# 	'''Computes the duration between 2 dates (that are in the same 24h interval), in minutes.'''
	# 	start = start.split('h')
	# 	end = end.split('h')
	# 	if start[0] > end[0]:
	# 		end[0] = int(end[0]) + 24
	# 	return (int(end[0]) - int(start[0])) * 60 + int(end[1]) - int(start[1])

	def getSum(self):
		return self._sum

	def reset(self, n=0):
		self._sum = n
	
	def __str__(self):
		return self.name + ' : ' + self.days().__str__()

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
	csvIn = sys.argv[1]
	args = sys.argv[2:]
	timesheet= TimeSheet(csvIn)
	bounds = []
	op = None
	options, remainder = getopt.getopt(args, 'b:a:', ['before=', 'after=', 'groups='])
	for opt, arg in options:
		if (opt in ('-a', '--after')):
			bounds = [arg] + bounds
			op = 'After'
		elif (opt in ('-b', '--before')):
			bounds += [arg]
			op = 'Before'
		elif (opt in ('--groups')):
			timesheet.setGroups(arg)
	if len(bounds) == 0:
		timesheet.sum()
	elif len(bounds) == 2:
		timesheet.sumBetween(bounds[0], bounds[1])
	else:
		getattr(timesheet, 'sum' + op)(bounds[0])
	print timesheet
