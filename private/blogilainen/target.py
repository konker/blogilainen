
import os
import logging


class Target(object):
    def __init__(self, source, physical_path, out_file, ext):
        self.source = source
        self.physical_path = physical_path
        self.virtual_path = "/%s" % source.relative_path
        self.out_file = out_file
        self.ext = ext
        self.out = os.path.join(self.physical_path, self.out_file) 
        
    def __repr__(self):
        return "Target[%s, %s, %s, %s]" % (self.out, self.physical_path, self.out_file, self.ext)

