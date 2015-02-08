import random
import interactive as ix
import reactive as rx

def load_file(path):
	with open(path) as f:
		return list(f.readlines())

class Dispenser():
	def __init__(self, messages, on_message, interval=5):
		assert messages is not None
		assert on_message is not None
		self.messages = messages
		self.on_message = on_message
		self.interval = interval
		self._counter = 0
	
	@property
	def is_running(self):
		try:
			self._stop
		except AttributeError:
			return False
		else:
			return True
	
	@property
	def progress(self):
		return self._counter, len(self.messages)
	
	def restart(self):
		assert self.is_running
		self.stop()
		self.start()
	
	def start(self):
		assert not self.is_running
		self._counter = 0
		playlist = ix.random_iter(self.messages)
		dispenser = rx.every_time_interval(self.interval, playlist)
		self._stop = dispenser.subscribe(self._on_message, self.restart)
	
	def stop(self):
		assert self.is_running
		self._stop()
		del self._stop
	
	def _on_message(self, message):
		self._counter += 1
		self.on_message(message)

class Repository():
	def __init__(self, messages, limit=None):
		assert messages is not None
		assert limit is None or limit > 0
		self.messages = messages
		self.limit = limit
		self._count = 0
	
	def is_locked(self):
		return self._count > self.limit
	
	def unlock(self):
		self._count = 0
	
	def random_message(self):
		if self.limit is not None:
			if self._count == self.limit:
				self._count += 1
				raise LimitExceededError()
			if self._count > self.limit:
				raise LockedError()
		self._count += 1
		return random.choice(self.messages)

class LimitExceededError(Exception):
	pass

class LockedError(Exception):
	pass
