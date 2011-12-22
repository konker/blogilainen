
import os
import logging


class Source(object):
    def __init__(self, srcpath, relpath, srcfile):
        self.targets = {}
        self.srcpath = srcpath
        self.relpath = relpath
        self.srcfile = srcfile
        self.src = os.path.join(self.srcpath, self.srcfile) 

    def add_target(self, target):
        self.targets[target.ext] = target
        
    def __repr__(self):
        return "Source[%s, %s, %s, %s] -> %s" % (self.src, self.srcpath, self.relpath, self.srcfile, self.targets)
