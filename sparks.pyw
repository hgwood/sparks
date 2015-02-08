"""
Sparks 2, by Hugo Wood, public domain.

Revision log
	2.0 (2012/15/03)
		- complete rewrite from Sparks 1
		- new: timezone awareness
		- new: daylight saving time awareness
		- new: configurability
		- new: playlist randomness instead of total randomness
		- new: displayed messages counter
	2.1 (2012/17/03)
		- new: milestone messages
		- fix: message dispenser
		- fix: update timer
		2.1.1 (2012/19/03)
			- fix: message dispenser

Todo
	- anniversaries

"""

def convert_module(path):
	import messages
	lines = '\n'.join(messages.messages)
	with open(path, 'w') as f:
		f.writelines(lines)

if __name__ == '__main__':
	import sys
	if len(sys.argv) == 1:
		import ui
		ui.run()
	elif sys.argv[1] == 'c':
		convert_module(sys.argv[2])
	else:
		print('Usage:')
		print('sparks.pyw to launch the UI')
		print('sparks.pyw c path to convert module messages to message file')
	