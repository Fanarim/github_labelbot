#!/usr/bin/env python3

import click

from labelbot import LabelBot, UrlParam


@click.group()
@click.option('--token-file',
              '-t',
              type=click.Path(exists=True,
                              file_okay=True,
                              readable=True),
              default='token.cfg',
              help='file containing GitHub token information')
@click.option('--rules-file',
              '-u',
              type=click.Path(exists=True,
                              file_okay=True,
                              readable=True),
              default='rules.cfg.sample',
              help='file containing issues labeling rules')
@click.option('--default-label',
              '-d',
              help='default label to use after no rule is matched')
@click.option('--check-comments',
              '-c',
              is_flag=True,
              help='flag indicating comments should also be checked')
@click.option('--skip-labeled',
              '-s',
              is_flag=True,
              help='skip labeling issues that already have any label')
def cli(token_file, rules_file, default_label, check_comments, skip_labeled):
    pass


@cli.command(short_help='Run console daemon periodically checking issues')
@click.option('--interval',
              '-i',
              type=int,
              default=10,
              help='time interval in seconds in which to check issues')
@click.argument('repo_urls',
                nargs=-1,
                required=True,
                type=UrlParam())
def console(interval, repo_urls):
    labelbot = LabelBot(token_file, rules_file, default_label, interval,
                        check_comments, skip_labeled)
    labelbot.add_repos(repo_urls)
    labelbot.run()


@cli.command(short_help='Run web API listening for issue updates')
def web():
    pass

if __name__ == '__main__':
    cli()
