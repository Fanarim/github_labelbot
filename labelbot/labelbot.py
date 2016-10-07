#!/usr/bin/env python3

import click
import re
import requests
import sched
import sys
import time
import validators


class LabelBot(object):
    def __init__(self, token_file, rules_file, default_label, interval,
                 check_comments, recheck):
        self.last_issue_checked = 0
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.default_label = default_label
        self.interval = interval
        self.check_comments = check_comments
        self.recheck = recheck

        # get GitHub token
        self.token = self._get_token(token_file)

        # get request session and validate token
        self.session = self._get_requests_session(self.token)

        # load and validate rules
        self.rules = self._get_rules(rules_file)

        # TODO check issues
        # for rule in self.rules:
        #     if rule.pattern.findall(issue_content):
        #         add_label(rule.label)

    def add_repos(self, repos):
        """Add repos and start labeling them"""
        # start labeling issues in given repos
        for repo in repos:
            self.scheduler.enter(0, 1, self._label_issues,
                                 argument=(repo, self.interval,))
        self.scheduler.run()

    def _label_issues(self, repo, interval):
        print("Checking issues in " + repo)
        self.scheduler.enter(self.interval, 1, self._label_issues,
                             argument=(repo, self.interval,))

    def _get_rules(self, rules_file):
        """Get labeling rules from the provided file"""
        # TODO improve rules validation
        rules = []
        with open(rules_file) as rules_file:
            for line in rules_file.readlines():
                words = line.splitlines()[0].split('::')
                print(words)
                if len(words) != 2:
                    print("Skipping invalid rule. ", file=sys.stderr)
                    continue
                rules.append(LabelingRule(words[0], words[1]))
        return rules

    def _get_token(self, token_file):
        """Get GitHub token from the provided file"""
        with open(token_file) as token_file:
            token = token_file.readline().splitlines()[0]

        return token

    def _get_requests_session(self, token):
        """Returns a requests session and verifies valid GitHub token was
        provided"""
        session = requests.Session()
        session.headers = {'Authorization': 'token ' + token,
                           'User-Agent': 'Python'}
        try:
            response = session.get('https://api.github.com/user')
        except:
            print('Could not connect to GitHub. Are you online? ')
            sys.exit(1)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            print('Couldn\'t connect to GitHub: ' +
                  str(response.status_code) +
                  ' - ' +
                  response.reason,
                  file=sys.stderr)

            if response.status_code == 401:
                print('Did you provide a valid token? ',
                      file=sys.stderr)

            sys.exit(1)

        return session


class UrlParam(click.ParamType):
    name = 'url'

    def convert(self, value, param, ctx):
        if not validators.url(value):
            self.fail('{} is not a valid URL. '.format(value), param, ctx)

        if 'github.com' not in value:
            self.fail('{} is not a GitHub URL. '.format(value), param, ctx)

        try:
            response = requests.get(value)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.fail('{} is not accessible. '.format(value), param, ctx)

        return value


class LabelingRule(object):
    def __init__(self, regex, label):
        self.pattern = re.compile(regex)
        print(self.pattern.pattern)
        self.label = label
