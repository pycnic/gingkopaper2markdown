# coding: utf-8
import configparser
import os
import sys

import click
import requests

GINGKO_API = 'https://gingkoapp.com/api'
GINGKO_API_EXPORT = GINGKO_API + '/export'

TEMPLATE = '''---
title: "{title}"
{headers}
abstract: "{abstract}"
---

{body}
'''

CONFIG_FILE = '.gingkopaper2markdown'
CONFIG_FILES = [
    CONFIG_FILE,
    os.path.join(
        os.getenv(
            'XDG_CONFIG_HOME',
            default=os.path.join(os.path.expanduser('~'), '.config'),
        ),
        CONFIG_FILE,
    )
]

# look for configuration file
config = configparser.ConfigParser()
config.read(CONFIG_FILES)
default_config = config['DEFAULT']
CONTEXT_SETTINGS = dict(
    default_map=dict(
        gingkopaper2markdown_cli=dict(default_config),
    )
)


def gingkopaper2markdown(
    gingko_user, gingko_password, gingko_treeid,
):

    try:
        gingko_url = GINGKO_API_EXPORT + '/' + gingko_treeid + '.txt?column='
    except TypeError:
        tb = sys.exc_info()[2]
        raise ValueError('gingkoapp treeid is missing').with_traceback(tb)

    # get export of title (column 1)
    column1 = requests.get(
                    gingko_url + '1',
                    auth=(gingko_user, gingko_password),
                )
    column1.raise_for_status()

    # parse export and extract title
    column1_lines = column1.text.splitlines()
    title = column1_lines[0].strip()[2:]
    headers = "\n".join(column1_lines[2:])

    # get export of abstract (column 2)
    column2 = requests.get(
                    gingko_url + '2',
                    auth=(gingko_user, gingko_password),
                )
    column2.raise_for_status()

    # parse export and extract abstract
    column2_lines = column2.text.splitlines()
    abstract = "\n".join(column2_lines[2:])

    # get export of paper (column 5)
    column5 = requests.get(
                    gingko_url + '5',
                    auth=(gingko_user, gingko_password),
                )
    column5.raise_for_status()

    # parse export and extract paper
    body = column5.text

    # write it to template
    return TEMPLATE.format(
        title=title,
        headers=headers,
        abstract=abstract,
        body=body,
    )


@click.command()
@click.option(
    '--user', '-u', help='gingkoapp username',
    default=default_config.get('user', None),
)
@click.option(
    '--password', '-p', help='gingkoapp password', hide_input=True,
    default=default_config.get('password', None),
)
@click.option(
    '--treeid', '-i', help='gingkoapp treeid',
    default=default_config.get('treeid', None),
)
@click.option(
    '--output', '-o', type=click.Path(), help='path to output file',
    default=default_config.get('output', None),
)
@click.option(
    '--force', '-f', is_flag=True,
    help='overwrite existing output file',
    default=default_config.get('force', False),
)
def gingkopaper2markdown_cli(
    user, password, treeid, output, force,
):
    result = gingkopaper2markdown(
        gingko_user=user,
        gingko_password=password,
        gingko_treeid=treeid,
    )
    if output:
        # open file for exclusive creation, raises exception if file already
        # exists
        with open(output, 'w' if force else 'x') as file:
            file.write(result)
    else:
        # output to stdout
        click.echo(result)


if __name__ == '__main__':
    gingkopaper2markdown_cli()
