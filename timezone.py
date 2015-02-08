from datetime import datetime, timedelta, tzinfo

parse = datetime.strptime

class DaylightSavingInfo():
	def __init__(self, start, end, offset=1):
		format = '%d/%m %H:%M'
		self.start = parse(start, format)
		self.end = parse(end, format)
		self.offset = timedelta(hours=offset)

class TimeZone(tzinfo):
	def __init__(self, name, utc_offset=0, dst_name=None, dst_info=None):
		self._name = name
		self._utc_offset = timedelta(hours=utc_offset)
		self._dst_info = dst_info
	
	def utcoffset(self, dt):
		return self._utc_offset + self.dst(dt)
	
	def dst(self, dt):
		assert dt is not None
		assert dt.tzinfo is self
		if self._dst_info is None:
			return timedelta(0)
		start = self._dst_info.start.replace(year=dt.year)
		end = self._dst_info.end.replace(year=dt.year)
		naive = dt.replace(tzinfo=None)
		def next_sunday(dt):
			days_to_sunday = 6 - dt.weekday()
			time_to_sunday = timedelta(days_to_sunday)
			return dt + time_to_sunday
		if next_sunday(start) < naive < next_sunday(end):
			return self._dst_info.offset
		return timedelta(0)
	
	def tzname(self, dt):
		if self.dst(dt):
			return self._dst_name
		return self._name

dst_ce = DaylightSavingInfo('25/03 02:00', '25/10 01:00')
dst_us = DaylightSavingInfo('08/03 02:00', '01/11 01:00')

utc = TimeZone('UTC')
central_european = TimeZone('CET', +1, 'CEST', dst_ce)
us_pacific = TimeZone('PST', -8, 'PDT', dst_us)