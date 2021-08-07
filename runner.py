"""Application Entry Point"""
from peewee import PostgresqlDatabase
from app import create_app, db
from app.models import ImageFile
import os
from os import environ
from peewee import *
from playhouse.db_url import connect # needed for peewee in heroku

# database = PostgresqlDatabases(DATABASE)
url = os.environ.get("DATABASE_URL") 
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)
db = connect(url)
print(f"DB URL = {url}")

def create_tables():
    with db:
        db.drop_tables([ImageFile])
        db.create_tables([ImageFile])

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'ImageFile': ImageFile}

if __name__ == '__main__':
    db.create_tables()
    app.run(debug=True)