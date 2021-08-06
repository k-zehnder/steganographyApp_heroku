from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey

from myapp import db

class ImageFile(db.Model):
    __tablename__ = 'ImageFile'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(300))
    text = db.Column(db.String(300))
    filename = db.Column(db.String(300), index=True)

    def __repr__(self):
        return f'{self.id}, {self.user}, {self.text}, {self.filename}'
