"""Flask app configuration."""
from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from environment variables."""

    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')

    # Flask-Uploads
    UPLOAD_PATH = environ.get('UPLOAD_PATH')
    DOWNLOAD_PATH = environ.get('DOWNLOAD_PATH')
    DECODED_PATH = environ.get('DECODED_PATH')

    # Upload Extentions
    UPLOAD_EXTENSIONS = environ.get('UPLOAD_EXTENSIONS')

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL") #environ.get("DATABASE_URL")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

