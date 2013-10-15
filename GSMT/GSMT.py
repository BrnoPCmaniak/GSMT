#-*- coding: utf8 -*-
import sqlite

class main(object):
    def __init__(self):
        self.path = "/etc/GSMT/"
        self.version = "1.1.1"
    
    def createSQLite(self):
        self.sqlite = sqlite.sqliteDriver(self, self.path)