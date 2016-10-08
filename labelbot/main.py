#!/usr/bin/env python3

import click

from labelbot import LabelBot, UrlParam


@click.command()
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
@click.option('--interval',
              '-i',
              type=int,
              default=10,
              help='time interval in seconds in which to check issues')
@click.option('--default-label',
              '-d',
              help='default label to use after no rule is matched')
@click.option('--check-comments',
              '-c',
              is_flag=True,
              default=True,
              help='flag indicating comments should also be checked')
@click.option('--skip-labeled',
              '-s',
              is_flag=True,
              default=False,
              help='skip labeling issues that already have any label')
@click.argument('repo_urls',
                nargs=-1,
                required=True,
                type=UrlParam())
def cli(repo_urls, token_file, rules_file, interval, default_label,
        check_comments, skip_labeled):
    labelbot = LabelBot(token_file, rules_file, default_label, interval,
                        check_comments, skip_labeled)
    labelbot.add_repos(repo_urls)
    labelbot.run()

if __name__ == '__main__':
    cli()
