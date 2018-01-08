#!/usr/bin/env python

import click

from flask import Flask

from database import db_init, db_session
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)
app.debug = True
graphql = GraphQLView.as_view('graphql', schema=schema, graphiql=True, context={'session': db_session})
app.add_url_rule('/graphql', view_func=graphql)


@click.command()
@click.option('--init', default=False, is_flag=True)
def main(init):
    if init:
        db_init()
        click.echo('Database initialized')
    app.run()


if __name__ == '__main__':
    main()
