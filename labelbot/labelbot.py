#!/usr/bin/env python3

import click


class LabelBot(object):

    @click.command()
    @click.option('--token-file',
                  '-t',
                  type=click.Path(),
                  help='file containing GitHub token information')
    @click.option('--repo',
                  '-r',
                  help='URL of repository this bot should operate on')
    @click.option('--rules-file',
                  '-u',
                  type=click.Path(),
                  help='file containing issues labeling rules')
    @click.option('--interval',
                  '-i',
                  type=int,
                  help='time interval in seconds in which to check issues')
    @click.option('--default-label',
                  '-d',
                  help='default label to use after no rule is matched')
    @click.option('--check-comments',
                  '-c',
                  is_flag=True,
                  help='flag indicating comments should also be checked')
    def run(repo, token_file, rules_file, interval, default_label,
            check_comments):
        """Run the command"""
        click.echo('Hello {}!'.format(token_file))
        print('Hello {}!'.format(token_file))
