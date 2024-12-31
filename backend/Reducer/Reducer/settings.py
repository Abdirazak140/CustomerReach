import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(ROOT_DIR)

from common.main_settings import *

ROOT_URLCONF = 'Reducer.urls'
WSGI_APPLICATION = 'Reducer.wsgi.application'