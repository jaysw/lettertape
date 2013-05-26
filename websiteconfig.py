import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = '42'
ELASTICSEARCH_HOST = 'http://192.168.0.8:9200'
ELASTICSEARCH_INDEX = 'songs'
del os
