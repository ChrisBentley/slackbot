from datetime import datetime
import time_fixer

crontable = []
outputs = []

channel = "C4G7HHCUW"  # TEST
# channel = "C2JJFADEY"  # Pegasus team

# crontable.append([60, "check_standup"])

def check_standup():
    # What time is it Mr.Wolf..?
    now = time_fixer.now()
    if now.weekday() < 5:
        # Today is a weekday!
        if now.hour == 9 and now.minute == 30:
            # It's 9:30am
            message = "@channel STANDUP {}\n===================================".format(now.strftime("%A, %d %B %Y"))
            outputs.append([channel, message])
