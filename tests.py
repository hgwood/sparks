import unittest
import timer

class TimedSequenceTest(unittest.TestCase):
	
	state = 0
	
	def increment_state(self, n):
		self.state += n
	
	class Timer():
		def __init__(self, function, *args, **kwargs):
			self.function = function
			self.args = args
			self.kwargs = kwargs
		def start(self):
			self.function(*self.args, **self.kwargs)
	
	def timer_generator(self):
		yield self.Timer(self.increment_state, 1)
	
	def test(self):
		seq = timer.TimedSequence(self.timer_generator())
		seq.start()
		self.assertTrue(self.state == 1)

if __name__ == '__main__':
    unittest.main()