#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# blogilainen
# 
# XML/XSLT based static web site generator
#
# Authors: Konrad Markus <konker@gmail.com>
#

import os
from blogilainen.blogilainen import Blogilainen

# FIXME: (some of) these should be options
SRC_DIR = 'src'
OUT_DIR = '../public'

XSLT_DIR = 'xslt'
XSLT = os.path.join(XSLT_DIR, 'index.xsl')

def main():
    blogilainen = Blogilainen(os.path.abspath(SRC_DIR), XSLT, os.path.abspath(OUT_DIR))
    blogilainen.generate()


if __name__ == '__main__':
    main()
