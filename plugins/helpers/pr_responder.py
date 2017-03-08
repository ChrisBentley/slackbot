import github_fetcher


def main():
    """
    This method fetches the current pull request data.
    """
    message = "Here are the pull requests you asked for:\n\n"
    message += github_fetcher.main()

    return message
