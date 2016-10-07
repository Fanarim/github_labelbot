#!/usr/bin/env python3

import requests
import sched
import sys
import time


class LabelBot(object):
    def __init__(self):
        self.last_issue_checked = 0
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def run(self, repo, token_file, rules_file, interval, default_label,
            check_comments, recheck):
        """Run the labelbot"""
        # get GitHub token
        token = self._get_token(token_file)

        # get request session and validate token
        self.session = self._get_requests_session(token)

        # start labeling issues
        self.scheduler.enter(0, 1, self._label_issues, argument=(interval,))
        self.scheduler.run()

    def _label_issues(self, interval):
        print("Doing stuff...")
        self.scheduler.enter(interval, 1, self._label_issues,
                             argument=(interval,))

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
