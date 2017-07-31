# Pegasus Bot

This is the slack bot used for team pegasus at M&S. Its most useful feature is the Pull Request Checker which informs the team about open PRs across our various repos.

Example output:
![Pegasus PR example](/doc/images/Pegasus-Bot.png?raw=true)


The bot is built using a [python real-time messaging bot](https://github.com/errror/python-rtmbot)

## Pegasus Bot Plugins
All of the additions made to our pegasus bot are available within the plugins directory.

Created Plugins
---------------
1. Standup.py
    * Notifies the pegasus team that it is time to have our standup.
2. Lunch.py
    * Notifies the pegsus team that it is time to go eat some lunch.
    * On specific days it will remind the team about good places to eat, for example the food market by MSQ on Thursdays.
3. pegasus_responder.py
    * Watches the pegsus channel for '@pegasus' and replies with relevant messages.
4. PR_checker.py
    * Notifies the pegasus team of all the open pull requests in their repos.
    * If a pull request is more than 2 days old it will be added to a separate list so that the team knows which PRs to prioritise.
    * Note - If you want to setup pr_checker.py you need to create your own github token that has read access to your repos. Place this token into a file called /plugins/helpers/github_token.py (an example version can be seen in this folder).

## Other Additions
---------------
When creating plugins that will be triggered at a certain time it is adviseable to use the helper script "time_fixer.py" to create a datetime object as has been done in all of the quick order plugins. This is so that the time when the plugin is triggered is correct irrespective of whether it is british summer time or if the server it is being ran from is using UTC or GMT time.


## Setting up your own slackbot
----------------------------

If you wish to setup your own slackbot you will need to create the bot as an integration within slack. (https://<team>.slack.com/services/new/bot)

You will then need to add the bot integration to the channel  of your choice (/invite @<botname> in your desired channel) and place the created slack token for the bot into a file called rtmbot.conf within the root directory of your repo.


## TODO list:
----------
- Add music suggestion feature inspiried by Tara
- Add meme generator ability similar to thinking Gavin
