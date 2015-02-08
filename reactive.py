from delay import map_delay, chain

class every_time_interval():
	"""
	A collection that pushes an item every specified period time.
	The first item is pushed after one period of time, not immediatly.
	
	"""
	def __init__(self, interval, iterable):
		"""
		:param interval: number of seconds between each push; must be greater 
			than 0
		:param iterable: items to push; cannot be None
		
		"""
		assert interval is not None
		assert interval > 0
		assert iterable is not None
		self.interval = interval
		self.iterable = iterable
	
	def subscribe(self, on_next, on_done=None):
		"""
		Subscribe to this collection.
		
		:param on_next: function to call when an item is pushed; cannot be None
		:param on_done: function to call when all items have been pushed;
			can be None
		:return: an object that can be called to unsubscribe
		
		"""
		assert on_next is not None
		actions = map_delay(self.interval, on_next, self.iterable)
		chained = chain(actions, on_done)
		chained.start()
		return chained.cancel

