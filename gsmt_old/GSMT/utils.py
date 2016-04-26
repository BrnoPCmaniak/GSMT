import hashlib, platform, os, getpass


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
    
    
def input(text, end):
    return SafeInput(raw_input, text, end)


def inputPass(text, end):
    return SafeInput(getpass.getpass, text, end)


def SafeInput(inputFunc, text, end):
    try:
        userInput = inputFunc(text)
        print "",
    except (EOFError, BaseException):
        print ""
        end()
    return userInput


class permission(object):
    def __init__(self, name, id):
        self.name = name
        self.id = id
