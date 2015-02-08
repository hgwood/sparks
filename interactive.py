import copy
import itertools
import random

def first(iterable):
	return next(iter(iterable))

def pairwise(iterable):
	first, second = itertools.tee(iterable)
	next(second, None)
	return itertools.zip_longest(first, second)

def prepend(first, iterable):
	yield first
	for item in iterable:
		yield item

def random_iter(iterable):
	a = copy.copy(iterable)
	random.shuffle(a)
	return iter(a)

class count_iter():
	def __init__(self, iterable):
		self._iterator = iter(iterable)
		self._index = 0
	
	def __iter__(self):
		return self
	
	def __next__(self):
		self._index += 1
		return next(self._iterator)
	
	@property
	def index(self):
		return self._index
