import sys
sys.path.insert(0, '.')
sys.path.append('vendor')

import web
from web.browser import AppBrowser
import web.test as webtest
from web.test import *  #including main

import settings
settings.db = web.database(dbn=os.environ.get('DATABASE_ENGINE', 'postgres'), db='watchdog_test')
db = settings.db
db.printing = False

import loaddb
loaddb.loaddb()

from webapp import app

debug = web.debug

class TestCase(webtest.TestCase):
    def setUp(self):
        self.t = db.transaction()
        self.ctx = dict(self.t.ctx)

    def tearDown(self):
        self.t.ctx = web.storage(self.ctx)
        self.t.rollback()

    def browser(self):
        self.b = AppBrowser(app)
        return self.b

    def login(self):
        self.b.open('http://watchdog.net/u/login')
        self.b.select_form(name='login')
        self.b['useremail'] = loaddb.test_email
        self.b['password'] = loaddb.test_passwd
        self.b.submit()

    def get_errors(self):
        soup = self.b.get_soup()
        errs = soup.findAll(attrs={'class': ['error', 'wrong']})
        return [self.b.get_text(e) for e in errs]
