import utils
class User(object):
    def __init__(self, id, Name, Password, blocked, changepass, permlist, sqlite):
        self.id = id
        self.name = Name
        self.password = Password
        self.blocked = blocked
        self.changepass = changepass
        self.permlist = permlist
        self.sqlite = sqlite
        self.star = False
        self.encryptPass = utils.encryptPass
        for perm in self.permlist:
            if perm.name == "*":
                self.star = True
    
    def changePass(self, old_password, new_password):
        if self.encryptPass(old_password) == self.password:
            self.password = self.encryptPass(new_password)
            self.updatePassword(self.password)
            return True
        else:
            return False
    
    def updatePassword(self, password):
        with self.sqlite.con:
            cur = self.con.cursor()
            cur.execute("UPDATE Users SET password='" + password + "' WHERE id=" + str(self.id) + "'")
    
    def updateBlocked(self, status):
        with self.sqlite.con:
            cur = self.con.cursor()
            if status == True:
                temp = str(0)
            else:
                temp = str(1)
            cur.execute("UPDATE Users SET blocked='" + temp + "' WHERE id=" + str(self.id) + "'")
    
    def updateChangePass(self, status):
        with self.sqlite.con:
            cur = self.con.cursor()
            if status == True:
                temp = str(0)
            else:
                temp = str(1)
            cur.execute("UPDATE Users SET changepass='" + temp + "' WHERE id=" + str(self.id) + "'")