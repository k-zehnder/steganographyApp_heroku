# from myapp import db
from peewee import *
import pandas as pd
import numpy as np
import datetime
from playhouse.db_url import connect
import os
from dotenv import load_dotenv

"""Note: from playhouse.db_url import connect
important import for using peewee in heroku"""
#db = connect(os.environ.get("DATABASE_URL")) # db = connect(os.environ.get('DATABASE_URL'))

url = os.environ.get("DATABASE_URL") 
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)
db = connect(url)

# Define your models here
class ImageFile(Model):
    user = TextField(null=True)
    filename = TextField(null=True)
    text = TextField(null=True)
    
    class Meta:
        database = db

# class ImageFile(db.Model):
#     __tablename__ = 'ImageFile'
#     id = db.Column(db.Integer, primary_key=True)
#     user = db.Column(db.String(300))
#     text = db.Column(db.String(300))
#     filename = db.Column(db.String(300), index=True)

#     def __repr__(self):
#         return f'{self.id}, {self.user}, {self.text}, {self.filename}'
