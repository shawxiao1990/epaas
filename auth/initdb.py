# -*- coding: utf-8 -*-

import click
from auth.extensions import db
from auth.models import User


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
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """init admin, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = User.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = User(
                username=username,
                name='Admin',
                introduction='Anything about you.'
            )
            admin.set_password(password)
            db.session.add(admin)

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    def forge():
        """Generate fake data."""
        from auth.fakes import fake_admin
        from auth.fakes import fake_role

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Generating the roles...')
        fake_role()

        click.echo('Done.')
