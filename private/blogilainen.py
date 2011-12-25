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
import sys
import logging
import optparse
from lxml import etree
from blogilainen.blogilainen import Blogilainen

DEFAULT_CONF_FILE='blogilainen-config.xml'
DEFAULT_LOG_FILE=None

DEFAULT_SOURCE_DIR = 'src'
DEFAULT_OUT_DIR = '../public'
DEFAULT_XSLT_FILE = os.path.join('xslt', 'index.xsl')
DEFAULT_RESOURCES_META_FILE = os.path.join('xslt', 'all-resources-meta.xml')


def read_options():
    # read in command line options
    parser = optparse.OptionParser()
    parser.add_option('-c', '--conf-file', dest='conf_file', default=DEFAULT_CONF_FILE, help="Config file location (defaults to %s)" % DEFAULT_CONF_FILE)
    parser.add_option('--log', dest='log_file', default=DEFAULT_LOG_FILE, help="where to send log messages (defaults to %s)" % DEFAULT_LOG_FILE)
    parser.add_option('--debug', dest='debug', action='store_true', default=False, help='Debug mode')
    options, args = parser.parse_args()
    if len(args) != 0:
        parser.error("Unknown arguments %s\n" % args)
    return options


def read_config(conf_file):
    xml = etree.parse(conf_file)
    source_dir = getattr(xml, 'source-dir', DEFAULT_SOURCE_DIR)
    out_dir = getattr(xml, 'out-dir', DEFAULT_OUT_DIR)
    xslt_file = getattr(xml, 'xslt-file', DEFAULT_XSLT_FILE)
    resources_meta_file = getattr(xml, 'resources-meta-file', DEFAULT_RESOURCES_META_FILE)

    return (source_dir, out_dir, xslt_file, resources_meta_file)


def setup_logging(log_file=None, debug=False):
    # set up logging
    if log_file:
        filename = log_file
        stream = None
    else:
        filename = None
        stream = sys.stderr

    datefmt = '%Y-%m-%d %H:%M:%S'

    if debug:
        level=logging.DEBUG
        format='%(asctime)s [%(threadName)s] %(message)s'
    else:
        level=logging.INFO
        format='%(asctime)s %(message)s'

    if stream:
        logging.basicConfig(level=level,
                            format=format,
                            stream=stream,
                            datefmt=datefmt)
    else:
        logging.basicConfig(level=level,
                            format=format,
                            filename=filename,
                            datefmt=datefmt)


def main():
    options = read_options()
    setup_logging(options.log_file, options.debug)
    source_dir, out_dir, xslt_file, resources_meta_file = read_config(options.conf_file)

    blogilainen = Blogilainen(
            os.path.abspath(source_dir),
            os.path.abspath(xslt_file),
            os.path.abspath(out_dir),
            os.path.abspath(resources_meta_file)
            )
    blogilainen.generate()


if __name__ == '__main__':
    main()
