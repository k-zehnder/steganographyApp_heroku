"""Main Views/Routes."""
import os
import base64
import cv2
import imutils
import numpy as np
from os import environ, path
from flask import Blueprint, render_template, make_response, redirect, url_for, current_app, request, send_from_directory, send_file, flash
from werkzeug.utils import secure_filename
from myapp.main.main_forms import UploadForm
from myapp.models import db, ImageFile
from myapp.utils import validate_image, my_decode_text, encode_text

main = Blueprint('main', __name__)

@main.route('/', methods=['GET','POST'])
def index():
    ds = ImageFile.query.all()
    files = os.listdir(current_app.config['UPLOAD_PATH'])

    # form presented to user here
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':#TODO: MUST BE PNG!!!!!

            # save uploaded photo to uploads folder
            uploaded_file.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))

            # encode message goes here
            encode_text(filename=filename, message=form.text.data)

            # db logic goes here
            image_file = ImageFile(
                text=form.text.data,
                filename=filename,
                user=form.name.data
            )
            db.session.add(image_file)
            db.session.commit()
            return redirect(url_for('main.thanks'))
    return render_template('_second_bootstrap.html', form=form, files=files, ds=ds)

@main.route('/all_files', methods=['GET','POST'])
def all_files():
    ds = ImageFile.query.all()
    files = os.listdir(current_app.config['UPLOAD_PATH'])
    return render_template('_show_entries.html', files=files, ds=ds)

@main.route('/thanks', methods=['GET', 'POST'])
def thanks():
    ds_all = ImageFile.query.all()
    ds = ds_all[-1]
    return render_template('_thanks_for_submitting.html', ds=ds)

@main.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST': # and form.validate_on_submit():
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            tempFile = ImageFile.query.all()[-1]
            message_to_show = my_decode_text(filename=filename)
            print(f"Message = {message_to_show}")
            return render_template('_decode.html', message_to_show=message_to_show, ds=tempFile)
    return redirect(url_for('main.index'))

@main.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)
