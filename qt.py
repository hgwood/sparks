import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

app = QApplication(sys.argv)

def exit():
	app.quit()

def run():
	sys.exit(app.exec_())

class TrayIcon():
	def __init__(self, icon, menu):
		self.q = QSystemTrayIcon()
		self.q.setIcon(QIcon(icon))
		self.q.setContextMenu(menu.q)
		self.q.show()
	def show_message(self, title, content):
		self.q.showMessage(title, content)

class Menu():
	
	class Item():
		def __init__(self, action):
			self.q = action
		@property
		def text(self):
			return self.q.text()
		@text.setter
		def text(self, value):
			self.q.setText(value)
	
	def __init__(self):
		self.q = QMenu()
	
	def __setattr__(self, name, value):
		if name == 'q': 
			object.__setattr__(self, name, value)
		else:
			self._add_item(name, value)
	
	def new_item(self, text=None, action=None):
		if text is None:
			text = '<menu_item>'
		qaction = self.q.addAction(text)
		if action is not None:
			qaction.triggered.connect(action)
		else:
			qaction.setEnabled(False)
		return self.Item(qaction)
	
	def _add_item(self, name, value):
		if isinstance(value, self.Item):
			item = value
		elif isinstance(value, str):
			item = self.new_item(value)
		else:
			item = self.new_item(value[0], value[1])
		object.__setattr__(self, name, item)

# The class holds its own instances so they are not garbage collected until 
# they have timed out.
_timers = []

class Timer():
	def __init__(self, interval, action, single_shot=False):
		self.q = QTimer()
		if single_shot:
			def remove():
				_timers.remove(id(self.q))
				action()
			self.q.timeout.connect(remove)
		else:
			self.q.timeout.connect(action)
		_timers.append(id(self.q))
		self.q.setSingleShot(single_shot)
		self.q.start(interval)