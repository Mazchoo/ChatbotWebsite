import time
import numpy as np

import django
from django.test.client import RequestFactory
from django.core.wsgi import get_wsgi_application
from django.test import Client
from main.common import *
from ChatBotWebsite.settings import ADMIN_USERNAME, ADMIN_PASSWORD

from unittest.mock import patch

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChatBotWebsite.settings")

django.setup()
application = get_wsgi_application()
CLIENT = Client()
REQ_FACTORY = RequestFactory()

def loginClient():
    CLIENT.login(username=ADMIN_USERNAME, password=ADMIN_PASSWORD)


def runAllTests(local_funcs):
    start_time = time.time()
    tests_passed = 0
    total_tests = 0

    for f_name, testFunction in local_funcs.items():
        if f_name[-5:] == '_test':
            total_tests += 1
            try:
                testFunction()
                tests_passed += 1
            except Exception as e:
                Logger.warn('Test Failed! ' + f_name)
                Logger.warn(e)

    time_taken = time.time() - start_time
    print('Total time taken:', np.round(time_taken, 2))
    print('Tests passed :', tests_passed, '/', total_tests)


def assertRaises(func, errorType, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except errorType:
        return True
    else:
        return False


def patchModelLoading(func):
    func = patch('dill.load')(func)
    func = patch('fastai.text.learner')(func)
    return patch('fastai.text.models.awdlstm')(func)
