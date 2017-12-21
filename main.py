#!/usr/bin/env python3

import click
from models import init_database


@click.command()
@click.option('--init', default=False, is_flag=True)
def main(init):
    if init:
        init_database()
        click.echo('Database initialized')


if __name__ == '__main__':
    main()
