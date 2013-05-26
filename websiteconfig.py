import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = '42'
ELASTICSEARCH_HOST = 'http://localhost:9200'
ELASTICSEARCH_INDEX = 'songs'
del os
