
import os
import sys
import logging
from lxml import etree
from source import Source
from target import Target

#import plugins.resource.enabled.get_meta_tags

RESOURCES_XML_DIR = 'xslt'
RESOURCES_XML = os.path.join(RESOURCES_XML_DIR, 'resources.xml')

BASE_PACKAGE = 'blogilainen.plugins'


class PluginException(Exception):
    pass


class Blogilainen(object):
    def __init__(self, srcdir, xslt, outdir):
        self.srcdir = srcdir
        self.xslt = xslt
        self.outdir = outdir

        self.sources = []
        self._load_sources()

        self.resource_plugins = {}
        self._load_resource_plugins()


    def generate(self):
        # generate the aggregate resources meta data and write it to file
        # XXX: param to govern overwriting of this file?
        # XXX: xslt hardcodes this file path?
        #resources_meta = self.generate_resources_meta()
        #print(etree.tostring(resources_meta, pretty_print=True))
        self.generate_resources_meta()

        # read in master xslt file
        transform = etree.XSLT(etree.parse(self.xslt))

        # go through each file and generate output
        for s in self.sources:
            xml = etree.parse(s.src)

            # generate for each target
            for ext,t in s.targets.iteritems():
                # make sure that outpath exists
                if not os.path.exists(t.outpath):
                    os.makedirs(t.outpath) 

                # execute XSLT transform and write output file
                with open(t.out, 'w') as fh:
                    fh.write(etree.tostring(transform(xml, format=etree.XSLT.strparam(t.ext))))

                print("%s -> %s" % (s.src, t.out))


    def generate_resources_meta(self):
        resources_meta = etree.Element('resources')

        for s in self.sources:
            resource = etree.Element('resource')
            for k, plugin in self.resource_plugins.iteritems():
                plugin.meta(s, resource)

            resources_meta.append(resource)

        with open(RESOURCES_XML, 'w') as fh:
            fh.write(etree.tostring(resources_meta, pretty_print=True))
            
        return resources_meta


    def _load_sources(self):
        for srcfile_path, dirnames, filenames in os.walk(self.srcdir):
            # get relative path starting from self.srcdir
            srcfile_relpath = os.path.relpath(srcfile_path, self.srcdir)

            get_formats = etree.XPath("//meta[@name='Format']/@content")
            for srcfile in filenames:
                if srcfile.endswith('.xml'):
                    # append a Source object to sources files list
                    source = Source(os.path.abspath(srcfile_path), srcfile_relpath, srcfile)
                    xml = etree.parse(source.src)
                    formats = get_formats(xml)

                    basename,ext = os.path.splitext(source.srcfile)
                    for format in formats:
                        outpath = os.path.abspath(os.path.join(self.outdir, source.relpath))
                        outfile = "%s.%s" % (basename, format)
                        target = Target(source, outpath, outfile, format)
                        source.add_target(target)

                    self.sources.append(source)
        #print(self.sources)


    def _load_resource_plugins(self):
        self._load_plugins('resource', self.resource_plugins)


    def _load_plugins(self, plugin_type, store):
        # read in and import available resource plugins
        #print(os.path.join(os.path.dirname(__file__), 'plugins', plugin_type, 'enabled'))
        module = None
        for py in os.listdir(os.path.join(os.path.dirname(__file__), 'plugins', plugin_type, 'enabled')):
            basename,ext = os.path.splitext(py)
            if ext != '.py' or py == '__init__.py':
                continue

            module = "%s.%s.enabled.%s" % (BASE_PACKAGE, plugin_type, basename)
            print("Found %s plugin: %s" % (plugin_type, module))
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

