from datetime import datetime
import time_fixer

crontable = []
outputs = []
# channel = "C4G7HHCUW"  # TEST
channel = "C2JJFADEY"  # Pegasus team

crontable.append([60, "check_standup"])

def check_standup():
    # What time is it Mr.Wolf..?
    now = time_fixer.now()
    if now.weekday() < 5:
        # Today is a weekday!
        if now.hour == 12 and now.minute == 0:
            # It's midday!
            message = "It's lunch time folks!"
            if now.weekday() == 3:
                # It's a Thursday!
                message += "\nCheck out the food market at MSQ"
            elif now.weekday() == 2 and (14 < now.day < 23):
                # It's the third Wednesday of the month!
                message += "\nRemember it's the KERB food market in Sheldon Square"
            outputs.append([channel, message])
