#!/usr/bin/env python3

import click

from labelbot import LabelBot


@click.command()
@click.option('--token-file',
              '-t',
              type=click.Path(exists=True,
                              file_okay=True,
                              readable=True),
              default='token.cfg',
              help='file containing GitHub token information')
@click.option('--repo',
              '-r',
              help='URL of repository this bot should operate on')
@click.option('--rules-file',
              '-u',
              type=click.Path(exists=True,
                              file_okay=True,
                              readable=True),
            #   default='rules.cfg',
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
@click.option('--recheck',
              '-r',
              is_flag=True,
              help='flag indicating all issues should be checked, \
                    not only the new ones')
def cli(repo, token_file, rules_file, interval, default_label,
        check_comments, recheck):
    labelbot = LabelBot()
    labelbot.run(repo, token_file, rules_file, interval, default_label,
                 check_comments, recheck)

if __name__ == '__main__':
    cli()
