# -*- coding: utf-8 -*-

import click
from epaas.extensions import db
from epaas.models import User, Role


def register_initdb_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    # @click.option('--username', prompt=True, help='The username used to login.')
    # @click.option('--password', prompt=True, hide_input=True,
    #               confirmation_prompt=True, help='The password used to login.')
    def init():
        """init admin, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = User.query.first()
        if admin is not None:
            click.echo('The administrator already exists, exit!')
        else:
            click.echo('Creating the temporary administrator account...')
            admin = User(
                username='admin',
                name='Admin',
                introduction='Anything about you.',
                roles="admin"
            )
            admin.set_password('password')
            db.session.add(admin)

            click.echo('Creating the default roles...')

            adminRole = Role(
                name='admin',
                description='Super Administrator. Have access to view all pages.'
            )
            editor = Role(
                name='editor',
                description='Normal Editor. Can see all pages except permission page.'
            )
            visitor = Role(
                name='visitor',
                description='Just a visitor. Can only see the home page and the document page.'
            )
            db.session.add(adminRole)
            db.session.add(editor)
            db.session.add(visitor)

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    def forge():
        """Generate fake data."""
        from epaas.fakes import fake_user
        from epaas.fakes import fake_role, fake_endpoint, fake_server

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_user()
        click.echo('Generating the roles...')
        fake_role()
        click.echo('Generating the endpoints...')
        fake_endpoint()
        click.echo('Generating the servers...')
        fake_server()
        click.echo('Done.')
