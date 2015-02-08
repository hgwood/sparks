import timezone as tz

# Clock Settings

girl_location = 'Evreux'
boy_location = 'San Diego'
girl_timezone = tz.central_european
boy_timezone = tz.us_pacific
separation_date = '2012/01/07 10:45', girl_timezone
reunion_date = '2012/04/21 20:30', boy_timezone
anniversaries = '23/04/11', '02/06/11', '11/06/11'

# Messaging Settings

# Fichier contenant les messages
message_file = 'messages.txt'
# Time between each automatic message
message_interval = 15 * 60 # seconds
# Number of messages that can be manually retrieved
message_retrieval_limit = 5
# Time before new messages can be manually retrieved after limit has been 
# reached
unlock_message_retrieval_after = 30 * 60 # seconds
# Interval between each progress milestone
milestone_interval = 5 # %

# UI Settings

icon_path = 'ghost.png'