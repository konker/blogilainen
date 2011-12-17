
import os
import logging


class Source(object):
    def __init__(self, srcpath=None, relpath=None, srcfile=None):
        self.srcpath = srcpath
        self.relpath = relpath
        self.srcfile = srcfile
        self.src = os.path.join(self.srcpath, self.srcfile) 

        
    def __repr__(self):
        return "Source[%s, %s, %s, %s]" % (self.src, self.srcpath, self.relpath, self.srcfile)
