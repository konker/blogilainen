
import os
import logging


class Target(object):
    def __init__(self, source, outpath, outfile, ext):
        self.source = source
        self.outpath = outpath
        self.outfile = outfile
        self.ext = ext
        self.out = os.path.join(self.outpath, self.outfile) 
        
    def __repr__(self):
        return "Target[%s, %s, %s, %s]" % (self.out, self.outpath, self.outfile, self.ext)

