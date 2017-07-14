#!/usr/bin/env python

import pygithub3
import github_token
import os
from pygithub3 import Github
from datetime import datetime

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_ORGANISATION = 'DigitalInnovation'
GITHUB_REPOS_DICT = ['mns-fe-starter-kit', 'fesk-store-listing', 'mns-core-ui', 'mns-core-ui-header', 'fesk-metrics', 'mns-core-test', 'mns-fe-foundation']


def get_all_valid_PRs(gh):

    valid_pull_requests = []

    # Check PRs for each repo (list of repos provided in config)
    for github_repo in GITHUB_REPOS_DICT:

        pull_requests_dict = gh.pull_requests.list(repo=github_repo).all()

        for pull_request in pull_requests_dict:
            # Check the PR's title for a comment that would invalidate it
            # and skip to the next PR in the list if one is found
            if 'do not merge' in pull_request.title.lower():
                continue
            if 'wip' in pull_request.title.lower():
                continue
            if 'spike' in pull_request.title.lower():
                continue
            else:
                # Append the repo name to the pr for later use
                pull_request.repo = github_repo
                # Add the PR to the list of valid PRs
                valid_pull_requests.append(pull_request)

    return valid_pull_requests


def count_comments_on_PR(gh, pr_number, pr_repo):

    pr = gh.pull_requests.get(pr_number, repo=pr_repo)

    comments = pr.comments + pr.review_comments

    return comments


def check_last_updated_time(updated_time):

    now = datetime.now()

    time_delta = now - updated_time

    return time_delta.days


def seal_url_fetcher(seal_type):
    # TODO make this function return random image urls
    # based on seal type instead of static images

    if seal_type == "angry":
        return "http://i.imgur.com/xFP7ts8.jpg"
    if seal_type == "informative":
        return "http://i.imgur.com/SAVH0Uv.jpg"
    if seal_type == "approval":
        return "http://i.imgur.com/AFkTE.png"

    return "http://i.imgur.com/PJeWltI.jpg"


def main(big_picture=False):

    # Setup a github API connection object using the organisation & a valid oAuth token
    gh = pygithub3.Github(user=GITHUB_ORGANISATION, token=GITHUB_TOKEN)

    # Create a dict containing all of the valid pull requests
    valid_pull_requests = get_all_valid_PRs(gh)

    # Initialise a message string
    message = ""

    if len(valid_pull_requests) == 0:
        message += ":seal_of_approval:  There are no pull requests that need reviewing!\n"
        if big_picture is True:
            seal_url = seal_url_fetcher("approval")
            message += "\n\nThe Seal of the day is: <" + seal_url + "|Seal of Approval>"
        return message

    # Setup a dict to hold any PRs older than 2 days
    older_pull_requests = []
    # Setup an info message string to hold the first set of PRs
    info_seal_message = ""

    for pr in valid_pull_requests:
        # Count the number of comments on the PR
        pr.comments_amount = count_comments_on_PR(gh, pr.number, pr.repo)
        # Get the username of the person who made the PR
        pr.username = pr.user['login']
        # Check how many days it's been since the PR was last updated
        pr.days_old = check_last_updated_time(pr.updated_at)

        # If the PR is more than 2 days old then add it to another dict for separate formatting
        if pr.days_old > 2:
            older_pull_requests.append(pr)
            # Skip to the next PR in the list
            continue

        # Format the PR info to be posted to slack
        info_seal_message += "*" + pr.repo + "*" + " | " + pr.username + " | " + "updated " + str(pr.days_old) + " days ago\n"
        info_seal_message += "<" + pr.html_url + "|" + pr.title + ">" + " - " + str(pr.comments_amount) + " comments\n\n"

    # Only append the info seal message if there are PRs less than 2 days old in the list
    if len(info_seal_message) > 0:
        message += "\n:informative_seal:  The following pull requests require your attention:\n\n" + info_seal_message

    # Only append the angry seal message if there are PRs more than 2 days old in the list
    if len(older_pull_requests) > 0:
        message += "\n:angrier_seal:  The following PRs haven't been updated in over 2 days!!!\n\n"

        for pr in older_pull_requests:
            message += "*" + pr.repo + "*" + " | " + pr.username + " | " + "updated " + str(pr.days_old) + " days ago\n"
            message += "<" + pr.html_url + "|" + pr.title + ">" + " - " + str(pr.comments_amount) + " comments\n\n"

    if big_picture is True:
        if "angrier_seal" in message:
            seal_url = seal_url_fetcher("angry")
            message += "\n\nThe Seal of the day is: <" + seal_url + "|Angry Seal>"
        else:
            seal_url = seal_url_fetcher("informative")
            message += "\n\nThe Seal of the day is: <" + seal_url + "|Informative Seal>"

    return message


(__name__ == '__main__' and main())
