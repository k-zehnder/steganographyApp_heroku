from flask_wtf import Form
from wtforms import StringField, FileField, SubmitField

class UploadForm(Form):
    text = StringField('Comment')
    name = StringField('Name')
    file = FileField('file')
    submit = SubmitField('submit')
