#!/usr/bin/env python3

import click

from flask import Flask
from flask_cors import CORS

from database import db_init, db_session
from fake import generate_fake_data
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)
CORS(app)
app.debug = True
graphql = GraphQLView.as_view('graphql', schema=schema, graphiql=True, context={'session': db_session})
app.add_url_rule('/graphql', view_func=graphql)


@click.command()
@click.option('--init', default=False, is_flag=True)
@click.option('--fake', default=False, is_flag=True)
def main(init, fake):
    if init:
        db_init()
        click.echo('Database initialized')
        if fake:
            click.echo('Populating fake data')
            generate_fake_data(3, 100)
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
