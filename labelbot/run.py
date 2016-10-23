#!/usr/bin/env python3

import click
# import console as labelbot_console
import os

from .console import run
from .labelbot import LabelBot, UrlParam
from .web import app


@click.group()
@click.option('--token-file',
              '-t',
              type=click.Path(exists=True,
                              file_okay=True,
                              readable=True),
              default='token.cfg.sample',
              help='file containing GitHub token information')
@click.option('--rules-file',
              '-u',
              type=click.Path(exists=True,
                              file_okay=True,
                              readable=True),
              default='rules.cfg.sample',
              help='file containing issues labeling rules')
@click.option('--github-token',
              '-g',
              help='github token used for authentication',
              default=lambda: os.environ.get('GITHUB_TOKEN'))
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
@click.pass_context
def cli(ctx, token_file, github_token, rules_file, default_label,
        check_comments, skip_labeled):
    ctx.obj = LabelBot(token_file, github_token, rules_file, default_label,
                       check_comments, skip_labeled)


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
@click.pass_obj
def console(labelbot, interval, repo_urls):
    run(labelbot, interval, repo_urls)


@cli.command(short_help='Run web API listening for issue updates')
@click.pass_obj
def web(labelbot):
    port = int(os.environ.get('PORT', 80))
    app.config['labelbot'] = labelbot
    app.run(host='0.0.0.0', port=port, debug=True)

cli(prog_name='labelbot')

def main():
    cli()
