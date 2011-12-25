
import os
import logging


class Target(object):
    def __init__(self, source, physical_path, basename, ext):
        self.source = source
        self.physical_path = physical_path
        #self.virtual_path = "%s" % source.relative_path
        self.out_path = source.relative_path
        self.out_file = "%s.%s" % (basename, ext)
        self.basename = basename
        self.ext = ext
        if source.relative_path == ".":
            self.out_url = self.out_file
        else:
            self.out_url = "%s/%s" % (source.relative_path, self.out_file)

        self.out = os.path.join(self.physical_path, self.out_file) 
        
    def __repr__(self):
        return "Target[%s, %s, %s, %s]" % (self.out, self.physical_path, self.out_file, self.ext)

