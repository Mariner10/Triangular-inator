#Throw those credentials in here!
import os


# Type of OS you are using, [macos or windows] 
# (macos is same as linux in terms of file system structure)
deviceType = "macos"

# If you want output printed to the terminal based on what the program is 
# doing live. (for logging or debugging purposes)
debugMode = False

# Email associated with the life360 account you are logging in with.
# Password to your life 360 account.
life360_username = "@gmail.com"
life360_password = ""

# Timezone you are operating from. i.e 'America/New_York' (You can run the program without selecting 
# a timezone and the program will print all timezones to choose from, then just paste 
# yours into the timeZone variable.
timeZone = 'America/New_York'

# Where the logs are stored on the separate server you'd want to download 
# them from. i.e "/home/pi/Triangular-inator/logs/"
remote_logs_directory = ""

# Where the logs are stored on your machine. 
# i.e "/Users/me/Desktop/Programming/Python/Triangular-inator/logs/"
local_logs_directory = ""

# These variables are for accessing a separate server to download 
# your data if it is not ran locally, if you have no intention on using 
# this function you can leave these blank.
serverHostname,serverPort,serverUser,serverPass = '192.168.1.1',22,'pi',''

# This is the gmail account that will be sending out updates to all the participants in the life360 circle!
yourGmail = "@gmail.com"

# this is the app password you can generate for the gmail account that allows it to send and receive mail.
# (look on the github for an link on how to do that!)
gmail_SENDING_appPass = ""




#Don't worry about these down here. It's only here for centralized access to the logs folders.
main_path = str(os.path.join(os.path.dirname(os.path.abspath(__file__))))
if deviceType == "windows":
    iHateWindows = "\logs\ "
    logPath = main_path + iHateWindows.strip()
else:
    logPath = main_path + "/logs/"