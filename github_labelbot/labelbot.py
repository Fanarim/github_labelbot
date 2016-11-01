#!/usr/bin/env python3

from posixpath import join as urljoin

import appdirs
import click
import json
import os
import re
import requests
import sched
import shutil
import sys
import time
import validators

module_path = os.path.dirname(__file__)


class LabelBot(object):
    """Class taking care of whole GitHub labeling bot's functionality. """
    github_api_url = 'https://api.github.com'
    repos_endpoint = urljoin(github_api_url, 'user/repos')
    issues_endpoint = urljoin(github_api_url,
                              'repos/{repo}/issues')
    issue_endpoint = urljoin(issues_endpoint, '{issue}')
    issue_comments_endpoint = urljoin(issue_endpoint,
                                      'comments')

    def __init__(self, token_file, github_token, rules_file, default_label,
                 check_comments, skip_labeled):
        config_dir = appdirs.user_config_dir('labelbot')

        # create/copy config files
        if token_file == "" and github_token == "":
            # create config dir
            if not os.path.exists(config_dir):
                os.mkdir(config_dir)
            source_file = os.path.join(module_path, 'token.cfg.sample')
            sample_token_file = os.path.join(config_dir,
                                             'token.cfg.sample')
            if not os.path.exists(sample_token_file):
                shutil.copyfile(source_file, sample_token_file)

        if rules_file == "":
            # create config dir
            if not os.path.exists(config_dir):
                os.mkdir(config_dir)
            source_file = os.path.join(module_path, 'rules.cfg.sample')
            sample_rules_file = os.path.join(config_dir,
                                             'rules.cfg.sample')
            if not os.path.exists(sample_rules_file):
                shutil.copyfile(source_file, sample_rules_file)

        # set default config files path if not set, get github token
        if token_file:
            self.token_file = token_file
        elif github_token:
            self.token = github_token
        else:
            print("Warning: You didn't set a GitHub token using -t or -u . "
                  "Using default config file at " + sample_token_file + ". ",
                  file=sys.stderr)
            self.token_file = sample_token_file
            self.token = self._get_token(self.token_file)

        if rules_file:
            self.rules_file = rules_file
        else:
            print("Warning: You didn't set a rules config file. Using default "
                  "file at " + sample_rules_file + ". ",
                  file=sys.stderr)
            self.rules_file = sample_rules_file

        self.last_issue_checked = 0
        self.iterval = 0
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.default_label = default_label
        self.check_comments = check_comments
        self.skip_labeled = skip_labeled

        # get request session and validate token
        self.session = self._get_requests_session(self.token)

        # load and validate rules
        self.rules = self._get_rules(self.rules_file)

        self._update_accessible_repos()

    def add_repos(self, repos):
        """Check provided URLs are valid GitHub repositories.
        Get full_name of each such repository and add labeling job for it.

        Args:
            repos: URLs of github repositories
        """
        # get list of valid user/repo values
        repo_names = []
        for repo in repos:
            found = False
            for available_repo in self.available_repos_json:
                if repo == available_repo['html_url']:
                    repo_names.append(available_repo['full_name'])
                    found = True
            if not found:
                print('Repository {} is not valid or bot is not allowed to '
                      'access it. '.format(repo), file=sys.stderr)

        # start labeling issues in given repos
        for repo in repo_names:
            self.scheduler.enter(0, 1, self._label_repo,
                                 argument=(repo,))

    def check_repo_accessible(self, repo):
        """Updates list of available repos and checks whether given repo is
        accessible by labelbot.

        Args:
            repo: full_name of github repository
        """
        # update available repos
        self._update_accessible_repos()

        if repo in [available_repo['full_name'] for available_repo
                    in self.available_repos_json]:
            return True
        else:
            return False

    def _update_accessible_repos(self):
        # TODO check status_code
        self.available_repos_json = self.session.get(
            self.repos_endpoint).json()

    def run_scheduled(self):
        """Initiate labeling by running a scheduler"""
        self.scheduler.run()

    def _label_repo(self, repo, reschedule=True):
        """Iterates through all issues in given repo and runs label_issue() on
        each of them.

        Args:
            repo: Full name of repository in form 'user/repo_name' as returned
            by GitHub API
        """

        print("Labeling issues in " + repo)

        # TODO do not check all issues, only the new ones
        # (based on user options)

        # get issues in given repo
        response = self.session.get(
            self.issues_endpoint.format(repo=repo))
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            print("Couldn't obtain necessary data from GitHub. ",
                  file=sys.stderr)
        issues = response.json()

        # iterate through all isues
        for issue in issues:
            self.label_issue(repo, issue)

        # run this again after given interval
        if reschedule:
            self.scheduler.enter(self.interval, 1, self._label_repo,
                                 argument=(repo,))

    def label_issue(self, repo, issue):
        """Iterates through an issue and labels it.

        Args:
            repo: Full name of repository in form 'user/repo_name' as returned
            by GitHub API
            issue: json interpretation of issue as returned by GitHub API
        """
        labels_to_add = []
        matched = False

        # get existing label strings
        existing_labels = [label['name'] for label in issue['labels']]

        # skip this issue if it is already labeled and skip_labeled
        # flag was used
        if self.skip_labeled and len(existing_labels) > 0:
            return

        # match rules in issue body and title
        for rule in self.rules:
            if rule.pattern.findall(issue['body'])\
                    or rule.pattern.findall(issue['title']):
                labels_to_add.append(rule.label)
                matched = True

        # match rules in issue comments if needed
        if self.check_comments:
            response = self.session.get(self.issue_comments_endpoint
                                        .format(
                                            issue=str(issue['number']),
                                            repo=repo))
            # TODO check status_code
            comments = response.json()
            for comment in comments:
                for rule in self.rules:
                    if rule.pattern.findall(comment['body']):
                        labels_to_add.append(rule.label)
                        matched = True

        # set default label if needed
        if self.default_label and matched == 0:
            labels_to_add.append(self.default_label)

        # set new labels
        labels_to_add = list(set(labels_to_add))  # make values unique
        new_labels = existing_labels + labels_to_add
        if not new_labels == existing_labels:
            response = self.session.patch(self.issue_endpoint.format(
                issue=str(issue['number']), repo=repo),
                data=json.dumps({'labels': new_labels}))

    def _get_rules(self, rules_file):
        """Parse labeling rules from the provided file.

        Args:
            rules_file: path to file containing rules - one line per rule
            in format regex::label
        """
        # TODO improve rules validation
        rules = []
        with open(rules_file) as rules_file:
            for line in rules_file.readlines():
                words = line.splitlines()[0].split('::')
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
        provided.

        Args:
            token: GitHub secret token

        Returns:
            Requests session with provided token, which can be used for
            communication with GitHub API.
        """
        session = requests.Session()
        session.headers = {'Authorization': 'token ' + token,
                           'User-Agent': 'Python'}
        try:
            response = session.get('https://api.github.com/user')
        except:
            print('Could not connect to GitHub. Are you online? ',
                  file=sys.stderr)
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
                print('Did you provide a valid token? You can specifiy it',
                      'using --github-token option. ',
                      file=sys.stderr)

            sys.exit(1)

        return session


class UrlParam(click.ParamType):
    """Class used for validating GitHub Repository URLs"""
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
    """Simple structure holding a single labeling rule"""
    def __init__(self, regex, label):
        self.pattern = re.compile(regex)
        self.label = label
