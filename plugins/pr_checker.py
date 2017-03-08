from datetime import datetime
import github_fetcher
import time_fixer

crontable = []
outputs = []
# channel = "C4G7HHCUW"  # TEST
channel = "C2JJFADEY"  # Pegasus team

crontable.append([60, "check_pr"])

def check_pr():
    # Check the time.
    now = time_fixer.now()
    # Check it's a weekday.
    if now.weekday() < 5:
        # Check if it's 9:45am
        if now.hour == 9 and now.minute == 45:
            message = "Good morning team! Here is today's pull request information...\n\n"
            message += github_fetcher.main(big_picture=False)
            outputs.append([channel, message])
