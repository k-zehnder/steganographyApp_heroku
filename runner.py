"""Application Entry Point"""
from peewee import PostgresqlDatabase
from app import create_app, db
from app.models import ImageFile
import os
from os import environ
from peewee import *
from playhouse.db_url import connect # needed for peewee in heroku

app = create_app()


# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'ImageFile': ImageFile}

if __name__ == '__main__':
    app.run(debug=True)