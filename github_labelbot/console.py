#!/usr/bin/env python3


def run(labelbot, interval, repo_urls):
    """Run LabelBot in console mode. Repositories are labeled periodically
    based on given interval.

    Args:
        interval (int): Interval in which repositories should be re-checked.
        repo_urls (:obj:`list` of :obj:`str`): List of repository URLs to be
            checked by labelbot.
    """
    labelbot.interval = interval
    labelbot.add_repos(repo_urls)
    labelbot.run_scheduled()
