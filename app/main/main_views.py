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
from app.utils import validate_image, my_decode_text, encode_text, my_decode_text_two
from PIL import Image
import io
import cv2
import numpy as np
import base64

#### temp
from peewee import *
from playhouse.db_url import connect # needed for peewee in heroku

main = Blueprint('main', __name__)
project_root = os.path.dirname(os.path.dirname(__file__))
UPLOADS = os.path.join(project_root, current_app.config['UPLOAD_PATH'])
DOWNLOADS = os.path.join(project_root, current_app.config['DOWNLOAD_PATH'])
DECODED = os.path.join(project_root, current_app.config['DECODED_PATH'])
print(f"TEST: {(UPLOADS, DOWNLOADS, DECODED)}")


url = os.environ.get("DATABASE_URL") 
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)
db = connect(url)
print(f"DB URL = {url}")
db.connect()
#db.drop_tables([ImageFile])
# db.create_tables([ImageFile])

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
            
            # encode message goes here (saves to DOWNLOADS)
            encode_text(filename=filename, message=form.text.data)

            # db logic goes here
            ImageFile.create(
                user=form.name.data,
                filename=filename,
                text=form.text.data,
            )
            db.close()
            
            query = ImageFile.get(ImageFile.filename == filename).filename
            print(f"QUERY: {query}")

            return redirect(url_for('main.thanks', filename=query))
    return render_template('_second_bootstrap.html', form=form, files=files, ds=ds)

@main.route('/all_files', methods=['GET','POST'])
def all_files():
    ds = ImageFile.select()
    files = [f for f in os.listdir(UPLOADS)]
    print(files)

    return render_template('_show_entries.html', files=files, ds=ds)

@main.route('/thanks/<filename>', methods=['GET', 'POST'])
def thanks(filename):
    ds = ImageFile.select().where(ImageFile.filename==filename)
    return render_template('_thanks_for_submitting.html',filename=filename, ds=ds)

@main.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST': # and form.validate_on_submit():
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            uploaded_file.save(os.path.join(DECODED, filename))

            # db logic goes here
            ImageFile.create(
                user=request.values.get('name'),
                filename=filename,
                text=request.values.get('text'),
            )
            db.close()

            query = ImageFile.get(ImageFile.filename == filename).filename

            #message_to_show = my_decode_text(filename=filename)
            message_to_show = my_decode_text_two(filename=query)
            print(f"Message = {message_to_show}")
            return render_template('_decode.html', message_to_show=message_to_show, query=query)
    return redirect(url_for('main.index'))

@main.route('/get_upload/<filename>')
def get_upload(filename):
    return send_from_directory(DOWNLOADS, "encoded_" + filename)

@main.route('/get_encoded/<filename>')
def get_decoded(filename):
    return send_from_directory(DECODED, filename)