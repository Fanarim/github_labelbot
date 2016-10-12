#!/usr/bin/env python3


def run(labelbot, interval, repo_urls):
    labelbot.interval = interval
    labelbot.add_repos(repo_urls)
    labelbot.run()
