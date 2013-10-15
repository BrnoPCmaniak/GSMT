#-*- coding: utf8 -*-
import sqlite

class main(object):
    def __init__(self, config=True):
        self.path = "/etc/GSMT/"
        self.version = "1.1.0"
        if not config:
            self.sqlite = sqlite.sqliteDriver(self)
        else:
            self.sqlite = None
    
    def createSQLite(self):
        self.sqlite = sqlite.sqliteDriver(self)