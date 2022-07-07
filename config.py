import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'glory-glory-man-utd'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'absen.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = 'app/static/upload'


  



