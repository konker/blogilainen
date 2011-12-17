
import os
import sys
import logging
from lxml import etree
from source import Source

#import resource.plugins.enabled.get_meta_tags

RESOURCES_XML_DIR = 'xslt'
RESOURCES_XML = os.path.join(RESOURCES_XML_DIR, 'resources.xml')

PACKAGE = 'blogilainen.resource.plugins.enabled'


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
        resources_meta = self.generate_resources_meta()
        print(etree.tostring(resources_meta, pretty_print=True))
        with open(RESOURCES_XML, 'w') as f:
            f.write(etree.tostring(resources_meta, pretty_print=True))

        # read in master xslt file
        transform = etree.XSLT(etree.parse(self.xslt))
        get_formats = etree.XPath("//meta[@name='Format']/@content")

        # go through each file and generate output
        for s in self.sources:
            src = os.path.join(s.srcpath, s.srcfile) 
            xml = etree.parse(src)
            formats = get_formats(xml)

            basename,ext = os.path.splitext(s.srcfile)
            for format in formats:
                outfile = "%s.%s" % (basename, format)
                outpath = os.path.abspath(os.path.join(self.outdir, s.relpath))
                out = os.path.join(outpath, outfile)
                print(outpath)

                # make sure that outpath exists
                if not os.path.exists(outpath):
                    os.makedirs(outpath) 

                # execute XSLT transform and write output file
                with open(out, 'w') as f:
                    f.write(etree.tostring(transform(xml)))

                print("%s -> %s" % (src, out))


    def generate_resources_meta(self):
        aggregate_meta = etree.Element('resources')

        for s in self.sources:
            resource = etree.Element('resource')
            for k, plugin in self.resource_plugins.iteritems():
                plugin.meta(s, resource)

            aggregate_meta.append(resource)
        return aggregate_meta


    def _load_sources(self):
        for srcfile_path, dirnames, filenames in os.walk(self.srcdir):
            # get relative path starting from self.srcdir
            srcfile_relpath = os.path.relpath(srcfile_path, self.srcdir)

            for srcfile in filenames:
                if srcfile.endswith('.xml'):
                    # append a Source object to sources files list
                    self.sources.append(Source(os.path.abspath(srcfile_path), srcfile_relpath, srcfile))

        print(self.sources)


    def _load_resource_plugins(self):
        # read in and import available resource plugins
        print(os.path.join(os.path.dirname(__file__), 'resource', 'plugins', 'enabled'))
        module = None
        for py in os.listdir(os.path.join(os.path.dirname(__file__), 'resource', 'plugins', 'enabled')):
            basename,ext = os.path.splitext(py)
            if ext != '.py' or py == '__init__.py':
                continue

            module = "%s.%s" % (PACKAGE, basename)
            print("Found plugin: %s" % module)
            cls = 'Plugin'
            try:
                __import__(module, locals(), globals())
            except:
                logging.error('Could not import module %s' % module)
                raise PluginException('Could not import module %s' % module)

            if sys.modules.has_key(module):
                if hasattr(sys.modules[module], cls):
                    self.resource_plugins[module] = getattr(sys.modules[module], cls)()
                else:
                    logging.error('Module has no class %s' % cls)
                    raise PluginException('Module has no class %s' % cls)
            else:
                logging.error('Could not import module %s' % module)
                raise PluginException('Could not import module %s' % module)

        del module

