
import os
import logging


class Source(object):
    def __init__(self, source_path, relative_path, source_file):
        self.targets = {}
        self.source_path = source_path
        self.relative_path = relative_path
        self.source_file = source_file
        self.basename,self.ext = os.path.splitext(self.source_file)
        if self.ext[0] == '.':
            self.ext = self.ext[1:]

        if self.relative_path == ".":
            self.source_url = self.source_file
        else:
            self.source_url = "%s/%s" % (self.relative_path, self.source_file)

        self.source = os.path.join(self.source_path, self.source_file) 

    def add_target(self, target):
        self.targets[target.ext] = target
        
    def __repr__(self):
        return "Source[%s, %s, %s, %s] -> %s" % (self.source, self.source_path, self.relative_path, self.source_file, self.targets)
