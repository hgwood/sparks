import datetime
import os
import clock
import messaging
import qt
import settings
import strings
import timezone as tz

windows = os.name == 'nt'

def run():
	qt.run()

def exit():
	if dispenser.is_running:
		dispenser.stop()
	qt.exit()

def show_notification(title, content):
	if not windows or len(title) < 64:
		icon.show_message(title, content)
	elif len(content) < 64:
		icon.show_message(content, title)
	else:
		icon.show_message(strings.default_title, title + os.linesep + content)

def show_message(message):
	show_notification(message, menu.remaining_nights.text)

def show_pulled_message():
	try:
		message = repository.random_message()
	except messaging.LimitExceededError:
		message = strings.request_limit_reached
		qt.Timer(settings.unlock_message_retrieval_after * 1000, 
			repository.unlock, single_shot=True)
	except messaging.LockedError:
		message = strings.request_limit_reached
	show_message(message)

def show_pushed_message(message):
	shown,total = dispenser.progress
	menu.message_counts.text = strings.dispenser_status.format(shown, total)
	show_message(message)

def switch_dispenser():
	if dispenser.is_running:
		dispenser.stop()
		menu.dispenser_switch.text = strings.enabled_dispenser
	else:
		dispenser.start()
		show_pushed_message(strings.dispenser_enabled)
		menu.dispenser_switch.text = strings.disable_dispenser

def update():
	menu.girl_time.text = strings.time_format.format(
		settings.girl_location, tracker.girl_time)
	menu.boy_time.text = strings.time_format.format(
		settings.boy_location, tracker.boy_time)
	menu.remaining_nights.text = strings.remaining_nights.format(
		tracker.remaining_nights)
	menu.progression.text = strings.time_progression.format(
		tracker.progress)
	events.update(tracker.progress)

def event(milestone):
	show_message(strings.milestone_message.format(milestone))

# UI Building

menu = qt.Menu()
menu.girl_time = menu.new_item()
menu.boy_time = menu.new_item()
menu.remaining_nights = menu.new_item()
menu.progression = menu.new_item()
menu.message_counts = menu.new_item()
menu.dispenser_switch = strings.disable_dispenser, switch_dispenser
menu.request = strings.request_message, show_pulled_message
menu.quit = strings.exit, exit
icon = qt.TrayIcon(settings.icon_path, menu)

# Time Tracker Init

tracker = clock.TimeTracker(
	clock.date(*settings.separation_date), 
	clock.date(*settings.reunion_date), 
	settings.girl_timezone, 
	settings.boy_timezone)

milestones = clock.compute_milestones(
	tracker.progress, 
	settings.milestone_interval)
anniversaries = clock.compute_anniversaries(settings.anniversaries)

events = clock.EventManager(anniversaries, milestones, event)
update()
update_timer = qt.Timer(interval=1000, action=update)

# Messaging Init
try:
	messages = messaging.load_file(settings.message_file)
except:
	# show_notification(strings.error, strings.no_message_file)
	messages = [strings.default_message]
	strings.welcome_message = strings.no_message_file
repository = messaging.Repository(messages, settings.message_retrieval_limit)
dispenser = messaging.Dispenser(
	messages, show_pushed_message, settings.message_interval)
dispenser.start()
show_pushed_message(strings.welcome_message)

if __name__ == '__main__':
	# GO SPARKS GO!
	run()
