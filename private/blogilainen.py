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
from lxml import etree

SRC_DIR = 'src'
OUT_DIR = '../public'

XSLT_DIR = 'xslt'
XSLT = os.path.join(XSLT_DIR, 'index.xsl')
AGGREGATE_XSLT_DIR = os.path.join('xslt', 'aggregate')
AGGREGATE_XSLT = os.path.join(AGGREGATE_XSLT_DIR, 'index.xsl')

def main():
    sources = []
    for srcpath, dirnames, filenames in os.walk(SRC_DIR):
        srcpath_parts = os.path.split(srcpath)
        if len(srcpath_parts) > 0 and srcpath_parts[0] == '':
            # annoying
            srcpath_parts = srcpath_parts[1:]

        for srcfile in filenames:
            if srcfile.endswith('.xml'):
                if len(srcpath_parts) > 1:
                    basepath = os.path.join(*srcpath_parts[1:]) 
                else:
                    basepath = ''

                # append a tuple to sources files list (note trailing , to force tuple)
                sources.append((os.path.abspath(srcpath), basepath, srcfile,))
    print(sources)

    # generate the aggregate meta data
    aggregate_meta = generate_aggregate_meta(sources)
    print(etree.tostring(aggregate_meta, pretty_print=True))

    # read in master xslt file
    transform = etree.XSLT(etree.parse(XSLT))

    get_formats = etree.XPath("//meta[@name='Format']/@content")
    # go through each file and generate output
    for srcpath,basepath,srcfile in sources:
        src = os.path.join(srcpath, srcfile) 
        xml = etree.parse(src)
        xml.getroot().append(aggregate_meta)
        print(etree.tostring(xml, pretty_print=True))
        formats = get_formats(xml)

        basename,ext = os.path.splitext(srcfile)
        for format in formats:
            outfile = "%s.%s" % (basename, format)
            outpath = os.path.abspath(os.path.join(OUT_DIR, basepath))
            out = os.path.join(outpath, outfile)

            # make sure that outpath exists
            if not os.path.exists(outpath):
                os.makedirs(outpath) 

            # execute XSLT transform and write output file
            with open(out, 'w') as f:
                f.write(etree.tostring(transform(xml), pretty_print=True))

            print(src, '->', out)


def generate_aggregate_meta(sources):
    transform = etree.XSLT(etree.parse(AGGREGATE_XSLT))
    aggregate_meta = etree.Element('resources')

    for srcpath,basepath,srcfile in sources:
        # execute AGGREGATE_XSLT against src file
        src = os.path.join(srcpath, srcfile) 
        xml = etree.parse(src)
        meta = transform(xml).getroot()

        # add some extra meta elements
        meta.append(etree.Element('meta', name='srcpath', content=srcpath))
        meta.append(etree.Element('meta', name='basepath', content=basepath))
        meta.append(etree.Element('meta', name='srcfile', content=srcfile))
        meta.append(etree.Element('meta', name='src', content=src))

        # add result to aggregate_meta
        aggregate_meta.append(meta)

    return aggregate_meta

if __name__ == '__main__':
    main()
