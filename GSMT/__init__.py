#-*- coding: utf8 -*-

__version__ = '1.3.3'
import GSMT, os
try:
    with open('/etc/GSMT/config'): pass
except IOError as e:
    print "GSMT is not configured!"
    print "Try to run gsmt-configure!"
    
GSMT.main()
