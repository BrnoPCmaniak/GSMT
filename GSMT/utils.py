import hashlib
def encryptPass(password):
        md5 = hashlib.md5()
        md5.update(password)
        return md5.hexdigest()
class permission(object):
    def __init__(self, name, id):
        self.name = name
        self.id = id