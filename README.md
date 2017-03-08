python-rtmbot
=============
A Slack bot written in python that connects via the RTM API (part of the slack API).

Python-rtmbot is a callback based bot engine. The plugins architecture should be familiar to anyone with knowledge to the [Slack API](https://api.slack.com) and Python. The configuration file format is YAML.

Some differences to webhooks:

1. Doesn't require a webserver to receive messages
2. Can respond to direct messages from users
3. Logs in as a slack user (or bot)
4. Bot users must be invited to a channel

Dependencies
----------
* websocket-client https://pypi.python.org/pypi/websocket-client/
* python-slackclient https://github.com/slackhq/python-slackclient

Installation
-----------

1. Download the python-rtmbot code

        git clone git@github.com:slackhq/python-rtmbot.git
        cd python-rtmbot

2. Install dependencies ([virtualenv](http://virtualenv.readthedocs.org/en/latest/) is recommended.)

        pip install -r requirements.txt

3. Configure rtmbot (https://api.slack.com/bot-users)

        cp doc/example-config/rtmbot.conf .
        vi rtmbot.conf
          SLACK_TOKEN: "xoxb-11111111111-222222222222222"

*Note*: At this point rtmbot is ready to run, however no plugins are configured.

Add Plugins
-------

Plugins can be installed as .py files in the ```plugins/``` directory OR as a .py file in any first level subdirectory. If your plugin uses multiple source files and libraries, it is recommended that you create a directory. You can install as many plugins as you like, and each will handle every event received by the bot indepentently.

To install the example 'repeat' plugin

    mkdir plugins/repeat
    cp doc/example-plugins/repeat.py plugins/repeat

The repeat plugin will now be loaded by the bot on startup.

    ./rtmbot.py

Create Plugins
--------

####Incoming data
Plugins are callback based and respond to any event sent via the rtm websocket. To act on an event, create a function definition called process_(api_method) that accepts a single arg. For example, to handle incoming messages:

    def process_message(data):
        print data

This will print the incoming message json (dict) to the screen where the bot is running.

Plugins having a method defined as ```catch_all(data)``` will receive ALL events from the websocket. This is useful for learning the names of events and debugging.

####Outgoing data
Plugins can send messages back to any channel, including direct messages. This is done by appending a two item array to the outputs global array. The first item in the array is the channel ID and the second is the message text. Example that writes "hello world" when the plugin is started:

    outputs = []
    outputs.append(["C12345667", "hello world"])

*Note*: you should always create the outputs array at the start of your program, i.e. ```outputs = []```

####Timed jobs
Plugins can also run methods on a schedule. This allows a plugin to poll for updates or perform housekeeping during its lifetime. This is done by appending a two item array to the crontable array. The first item is the interval in seconds and the second item is the method to run. For example, this will print "hello world" every 10 seconds.

    outputs = []
    crontable = []
    crontable.append([10, "say_hello"])
    def say_hello():
        outputs.append(["C12345667", "hello world"])

####Plugin misc
The data within a plugin persists for the life of the rtmbot process. If you need persistent data, you should use something like sqlite or the python pickle libraries.

####Todo:
Some rtm data should be handled upstream, such as channel and user creation. These should create the proper objects on-the-fly.


Quick Order Additional Plugins
==============================
All of the additions made to our quick order bot are available within the plugins directory.

Created Plugins
---------------
1. Standup.py
    * Notifies the quick order team that it is time to have our standup.
2. Lunch.py
    * Notifies the quick order team that it is time to go eat some lunch.
    * On specific days it will remind the team about good places to eat, for example the food market by MSQ on Thursdays.
3. c3qo_responder.py
    * Watches the quick order channel for the key word 'c3qo' and replies with relevant messages.
4. PR_checker.py
    * Notifies the quick order team of all the open pull requests in their repos.
    * If a pull request is more than 2 days old it will be added to a separate list so that the team knows which PRs to prioritise.
    * Note - If you want to setup pr_checker.py you need to create your own github token that has read access to your repos. Place this token into a file called /plugins/helpers/github_token.py (an example version can be seen in this folder).

Setting up your own slackbot
----------------------------

If you wish to setup your own slackbot you will need to create the bot as an integration within slack. (https://<team>.slack.com/services/new/bot)

You will then need to add the bot integration to the channel  of your choice (/invite @<botname> in your desired channel) and place the created slack token for the bot into a file called rtmbot.conf within the root directory of your repo.


Other Additions
---------------
When creating plugins that will be triggered at a certain time it is adviseable to use the helper script "time_fixer.py" to create a datetime object as has been done in all of the quick order plugins. This is so that the time when the plugin is triggered is correct irrespective of whether it is british summer time or if the server it is being ran from is using UTC or GMT time.