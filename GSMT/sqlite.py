# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import user, utils

class sqliteDriver(object):
    def __init__(self, main):
        self.main = main
        self.con = None
        try:
            try:
                with open(self.main.path + 'database.db'): pass
            except IOError:
                file = open(self.main.path + 'database.db', "w")
                file.close()
            self.con = lite.connect(self.main.path + 'database.db')
            
            cur = self.con.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
            
            self.version = cur.fetchone()
        except lite.Error, e:
            
            print "Error %s:" % e.args[0]
            sys.exit(1)
    
    def create(self, name, password):
        with self.con:
            cur = self.con.cursor()    
            cur.execute("CREATE TABLE Users(id INT, name TEXT, password TEXT, blocked INT, changepass INT)")
            cur.execute("INSERT INTO Users VALUES(1,'" + str(name) + "', '" + str(password) + "', 1, 1)")
            cur.execute("CREATE TABLE perms(id INT, user INT, name TEXT)")
            cur.execute("INSERT INTO perms VALUES(1, 1, '*')")
    
    def getUserObject(self, name = None, id = None):
        with self.con:
            if name is not None and id is not None:
                cur = self.con.cursor()
                cur.execute("SELECT * FROM Users WHERE id = '" + str(id) + "'")
                userdata = cur.fetchone()
                cur2 = self.con.cursor()
                cur2.execute("SELECT * FROM perms WHERE id = '" + str(id) + "'")
                perms = cur2.fetchall()
                permlist = []
                for perm in perms:
                    permlist.append(utils.permission(perm[2], perm[0]))
                #              ID            Name      Password           Blocked                          Changepass
                return user.User(userdata[0], userdata[1], userdata[2], self.getBoolean(userdata[3]), self.getBoolean(userdata[4]), permlist, self)
            elif name is not None:
                cur = self.con.cursor()
                cur.execute("SELECT * FROM Users WHERE name = '" + str(name) + "'")
                userdata = cur.fetchone()
                cur2 = self.con.cursor()
                cur2.execute("SELECT * FROM perms WHERE id = '" + str(userdata[0]) + "'")
                perms = cur2.fetchall()
                print perms
                permlist = []
                for perm in perms:
                    permlist.append(utils.permission(str(perm[2]), str(perm[0])))
                #              ID            Name      Password           Blocked                          Changepass
                return user.User(userdata[0], userdata[1], userdata[2], self.getBoolean(userdata[3]), self.getBoolean(userdata[4]), permlist, self)
            elif id is not None:
                cur = self.con.cursor()
                cur.execute("SELECT * FROM Users WHERE id = '" + str(id) + "'")
                userdata = cur.fetchone()
                cur2 = self.con.cursor()
                cur2.execute("SELECT * FROM perms WHERE id = '" + str(id) + "'")
                perms = cur2.fetchall()
                permlist = []
                for perm in perms:
                    permlist.append(utils.permission(perm[2], perm[0]))
                #              ID            Name      Password           Blocked                          Changepass
                return user.User(userdata[0], userdata[1], userdata[2], self.getBoolean(userdata[3]), self.getBoolean(userdata[4]), permlist, self)
            else:
                return False
    
    def close(self):
        if self.con is not None:
            self.con.close()
    
    def getBoolean(self, status):
        return status == "0"