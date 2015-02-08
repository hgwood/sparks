import threading
import functools
import interactive as ix

def delay(interval, function, *args, **kwargs):
	assert interval is not None
	assert function is not None
	return threading.Timer(interval, function, args, kwargs)

def map_delay(interval, function, *iterables, **kwargs):
	partial_delay = functools.partial(delay, interval, function, **kwargs)
	return map(partial_delay, *iterables)

class chain():
	def __init__(self, timers, function=None, *args, **kwargs):
		# We don't know if it's an iterable or an iterator, and we need to 
		# iterate through the first element twice, so it is safer to treat it 
		# as an iterator.
		# Note: `list` could use a lot of memory, and `itertools.tee` is 
		# overkill for this case, since one of the iterator just need the 
		# first element.
		itimers = iter(timers)
		self._first = ix.first(itimers)
		self._cancel = False
		self.function = function
		self.args = args
		self.kwargs = kwargs
		for current,next in ix.pairwise(ix.prepend(self._first, itimers)):
			current.args = [next, current.function] + list(current.args)
			current.function = self._on_timer_elapsed
	
	def start(self):
		self._current = self._first
		self._first.start()
	
	def cancel(self):
		self._current.cancel()
	
	def _on_timer_elapsed(self, next, function, *args, **kwargs):
		function(*args, **kwargs)
		if next is not None:
			self._current = next
			next.start()
		else:
			self._on_all_elapsed()
	
	def _on_all_elapsed(self):
		if self.function is not None:
			self.function(*self.args, **self.kwargs)
