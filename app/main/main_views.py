"""Main Views/Routes."""
import os
import base64
import cv2
import imutils
import numpy as np
from os import environ, path
from dotenv import load_dotenv
from flask import Blueprint, render_template, make_response, redirect, url_for, current_app, request, send_from_directory, send_file, flash
from werkzeug.utils import secure_filename
from app.main.main_forms import UploadForm
from app.models import db, ImageFile
from app.utils import validate_image, my_decode_text, encode_text

#### temp
from peewee import *
from playhouse.db_url import connect # needed for peewee in heroku

main = Blueprint('main', __name__)
project_root = os.path.dirname(os.path.dirname(__file__))
UPLOADS = os.path.join(project_root, current_app.config['UPLOAD_PATH'])
DOWNLOADS = os.path.join(project_root, current_app.config['DOWNLOAD_PATH'])
print(f"TEST: {(UPLOADS, DOWNLOADS)}")

# url = os.getenv("DATABASE_URL")  # or other relevant config var
# if url.startswith("postgres://"):
#     url = url.replace("postgres://", "postgresql://", 1)
url = os.environ.get("DATABASE_URL") 
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)
db = connect(url)
print(f"DB URL = {url}")
db.connect()
db.drop_tables([ImageFile])
db.create_tables([ImageFile])

@main.route('/', methods=['GET','POST'])
def index():
    ds = ImageFile.select() # ds = ImageFile.query.all()
    files = os.listdir(os.path.join(project_root, current_app.config['UPLOAD_PATH']))
    # form presented to user here
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '': # MUST BE PNG!!!!!

            # save uploaded photo to uploads folder
            uploaded_file.save(os.path.join(UPLOADS, filename))
            
            # encode message goes here
            encode_text(filename=filename, message=form.text.data)

            # db logic goes here
            ImageFile.create(
                user=form.name.data,
                filename=filename,
                text=form.text.data,
            )
            db.close()
            return redirect(url_for('main.thanks'))
    return render_template('_second_bootstrap.html', form=form, files=files, ds=ds)

@main.route('/all_files', methods=['GET','POST'])
def all_files():
    ds = ImageFile.select()
    files = [f for f in os.listdir(UPLOADS)]
    print(files)

    return render_template('_show_entries.html', files=files, ds=ds)

@main.route('/thanks', methods=['GET', 'POST'])
def thanks():
    ds = ImageFile.select()
    ds = ds[-1]
    return render_template('_thanks_for_submitting.html', ds=ds)

@main.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST': # and form.validate_on_submit():
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            tempFile = ImageFile.select()[-1]
            message_to_show = my_decode_text(filename=filename)
            print(f"Message = {message_to_show}")
            return render_template('_decode.html', message_to_show=message_to_show, ds=tempFile)
    return redirect(url_for('main.index'))

@main.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(UPLOADS, filename)