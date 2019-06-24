import os
# You need to replace the next values with the appropriate values for your configuration

BASEDIR = os.path.abspath(os.path.dirname(__file__))
path = "sqlite:///{}".format(os.path.join(BASEDIR, 'db', '{}.db'))

SQLALCHEMY_DATABASE_URI = path.format('Server')
SQLALCHEMY_TRACK_MODIFICATIONS = True

