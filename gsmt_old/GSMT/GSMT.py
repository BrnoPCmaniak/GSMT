#-*- coding: utf8 -*-
import sqlite

class main(object):
    def __init__(self):
        self.path = "/etc/GSMT/"
        self.version = "1.3.6"
    
    def initSQLite(self):
        self.sqlite = sqlite.sqliteDriver(self, self.path)
