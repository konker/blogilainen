#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import markdown
from lxml import etree
from source import Source
from target import Target

#import plugins.resource.enabled.get_meta_tags
BASE_PACKAGE = 'blogilainen.plugins'


class PluginException(Exception):
    pass


class Blogilainen(object):
    def __init__(self, source_dir, xslt_file, out_dir, resources_meta_file):
        self.source_dir = source_dir
        self.xslt_file = xslt_file
        self.out_dir = out_dir
        self.resources_meta_file = resources_meta_file

        self.sources = []
        self._load_sources()

        self.resource_plugins = {}
        self._load_resource_plugins()

        logging.info("source_dir: %s" % self.source_dir)
        logging.info("xslt_file: %s" % self.xslt_file)
        logging.info("out_dir: %s" % self.out_dir)
        logging.info("resources_meta_file: %s" % self.resources_meta_file)


    def process_other(self, xml):
        xml_dash = self._process_markdown(xml)
        # ... could be others
        return xml_dash


    def _process_markdown(self, xml):
        get_markdown = etree.XPath("//markdown")
        markdowns = get_markdown(xml)
        for md in markdowns:
            print(md)
            #print(etree.tostring(m, pretty_print=True))
            md_parent = md.getparent()
            xml_s = "<div>%s</div>" % markdown.markdown(md.text) 
            print('---')
            print(xml_s)
            print('---')
            md_parent.replace(md, etree.fromstring(xml_s))
        return xml

    def generate(self):
        # generate the aggregate resources meta data and write it to file
        # XXX: param to govern overwriting of this file?
        self.generate_resources_meta()

        # read in master xslt file
        transform = etree.XSLT(etree.parse(self.xslt_file))

        # go through each file and generate output
        for s in self.sources:
            xml = etree.parse(s.source)

            # process markdown
            xml = self.process_other(xml)

            if len(s.targets) == 0:
                logging.info("WARNING: %s has no target formats" % s.source)

            # generate for each target
            for ext,t in s.targets.iteritems():
                # make sure that physical_path exists
                if not os.path.exists(t.physical_path):
                    os.makedirs(t.physical_path) 

                # execute XSLT transform and write output file
                with open(t.out, 'w') as fh:
                    content = etree.tostring(transform(xml, format=etree.XSLT.strparam(t.ext)))
                    if content:
                        fh.write(content)
                        logging.info("OK: %s -> %s" % (s.source, t.out))
                    else:
                        logging.info("FAILED: %s -> %s" % (s.source, t.out))


    def generate_resources_meta(self):
        resources_meta = etree.Element('resources')

        for s in self.sources:
            resource = etree.Element('resource')
            for k, plugin in self.resource_plugins.iteritems():
                plugin.run(s, resource)

            resources_meta.append(resource)

        with open(self.resources_meta_file, 'w') as fh:
            fh.write(etree.tostring(resources_meta, pretty_print=True))
            
        return resources_meta


    def _load_sources(self):
        for source_file_path, dirnames, filenames in os.walk(self.source_dir):
            # get relative path starting from self.source_dir
            source_file_relative_path = os.path.relpath(source_file_path, self.source_dir)

            get_formats = etree.XPath("//meta[@name='dcterms.Format']/@content")
            for f in filenames:
                # append a Source object to sources files list
                s = Source(os.path.abspath(source_file_path), source_file_relative_path, f)
                xml = etree.parse(s.source)
                formats = get_formats(xml)

                for ext in formats:
                    physical_path = os.path.abspath(os.path.join(self.out_dir, s.relative_path))
                    target = Target(s, physical_path, s.basename, ext)
                    s.add_target(target)
                    
                    # XXX: only use one format for now
                    break

                self.sources.append(s)
        logging.debug(self.sources)


    def _load_resource_plugins(self):
        self._load_plugins('resource', self.resource_plugins)


    def _load_plugins(self, plugin_type, store):
        # read in and import available resource plugins
        module = None
        for py in os.listdir(os.path.join(os.path.dirname(__file__), 'plugins', plugin_type, 'enabled')):
            basename,ext = os.path.splitext(py)
            if ext != '.py' or py == '__init__.py':
                continue

            module = "%s.%s.enabled.%s" % (BASE_PACKAGE, plugin_type, basename)
            logging.info("Found %s plugin: %s" % (plugin_type, module))
            cls = 'Plugin'
            try:
                __import__(module, locals(), globals())
            except:
                logging.error('Could not import module %s' % module)
                raise PluginException('Could not import module %s' % module)

            if sys.modules.has_key(module):
                if hasattr(sys.modules[module], cls):
                    # this is where the magic happens
                    store[module] = getattr(sys.modules[module], cls)()
                else:
                    logging.error('Module has no class %s' % cls)
                    raise PluginException('Module has no class %s' % cls)
            else:
                logging.error('Could not import module %s' % module)
                raise PluginException('Could not import module %s' % module)

        del module

