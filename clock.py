from datetime import date, datetime

today = date.today
now = datetime.now
parse = datetime.strptime

def date(datestr, tz=None):
	dt = parse(datestr, "%Y/%m/%d %H:%M")
	return dt.replace(tzinfo=tz)

class TimeTracker():
	def __init__(self, departure, arrival, girl_tz=None, boy_tz=None):
		self.departure = departure
		self.arrival = arrival
		self._duration = arrival - departure
		self.girl_tz = girl_tz
		self.boy_tz = boy_tz
	
	@property
	def girl_time(self):
		return now(self.girl_tz)
	
	@property
	def boy_time(self):
		return now(self.boy_tz)
	
	@property
	def progress(self):
		elapsed = now(self.departure.tzinfo) - self.departure
		return elapsed.total_seconds() / self._duration.total_seconds()
	
	@property
	def remaining_nights(self):
		remaining_time = self.arrival.date() - today()
		return remaining_time.days

def compute_milestones(progress, interval):
	progress *= 100
	next_milestone = int(progress - progress % interval + interval)
	milestones = range(next_milestone, 101, interval)
	return list(map(lambda x: x / 100, milestones))

def compute_anniversaries(dates):
	return []

class EventManager():
	def __init__(self, special_dates, milestones, callback):
		self.special_dates = special_dates
		self.milestones = milestones
		self.callback = callback
	def update(self, progress):
		if len(self.milestones) == 0:
			return
		if progress >= self.milestones[0]:
			milestone = self.milestones.pop(0)
			self.callback(milestone)