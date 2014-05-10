import hashlib, platform, os


def encryptPass(password):
        md5 = hashlib.md5()
        md5.update(password)
        return md5.hexdigest()


def checkPlatform():
    if platform.system() == "Linux":
        return True
    else:
        return False


def checkRoot():
    if os.geteuid()==0:
        return True
    else:
        return False
    
    
class permission(object):
    def __init__(self, name, id):
        self.name = name
        self.id = id