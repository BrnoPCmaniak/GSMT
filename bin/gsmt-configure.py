#!/usr/bin/python

import platform, os, sys
try: 
    import __init__
    #import imp
    #libMain = imp.load_source('GSMT', '../GSMT/__init__.py')
except Exception as e:
    print "Can't load main library!"
    print "ERROR: " + str(e)
    sys.exit()
#libMain = libMain.main()
libMain = main()
print "Welcome to GMST " + str(libMain.version) + " (c) Filip Dobrovolny 2013"
print "=========================="
if platform.system() != "Linux":
    print "Sorry platform: " + platform.system() + " is not supported yet :("
    print "Do you have supported platform and still showing this message plese contact us."
    sys.exit()
print "Platform: OK"
# if not root...kick out
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\n")
print "Root: OK"
try:
   with open('/etc/GSMT/config'): pass
except IOError:
   print 'GSMT alredy exists.'
   print 'If GSMT not exists, please try remove /etc/GSMT folder'
   sys.exit()
print "/etc/GSMT not exist: OK"
try:
    os.mkdir("/etc/GSMT")
except Exeption, e:
    print "Uknown error at creting /etc/GSMT folder. Please report bug."
    print "ERROR: " + str(e) + " " + str(e.name)
    sys.exit()
print "/etc/GSMT created: OK"
try:
    os.mkdir("/etc/GSMT/games")
except Exeption, e:
    print "Uknown error at creting /etc/GSMT/games folder. Please report bug."
    print "ERROR: " + str(e) + " " + str(e.name)
    sys.exit()
print "/etc/GSMT/games created: OK"
try:
    os.mkdir("/etc/GSMT/modules")
except Exeption, e:
    print "Uknown error at creting /etc/GSMT/modules folder. Please report bug."
    print "ERROR: " + str(e) + " " + str(e.name)
    sys.exit()
print "/etc/GSMT/modules created: OK"
print "please create superuser:"
name = raw_input("name:")
while True:
    password1 = raw_input("password:")
    if password1 == "q":
        print "Exitting ..."
        print "Create superuser: Failed"
        sys.exit()
        break
    password2 = raw_input("re-password:")
    if password1 == password2:
        break
    else:
        print "Password aren't same please try it again. Press q to exit."
try:
    libMain.sqlite.create(name, password1)
except Exeption, e:
    print "Uknown error at creting sqlite database. Please report bug."
    print "ERROR: " + str(e) + " " + str(e.name)
    sys.exit()
print "SQLite created: OK"
print "Superuser created: OK"
