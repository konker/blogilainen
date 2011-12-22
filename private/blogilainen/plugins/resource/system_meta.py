
import logging
from lxml import etree
from blogilainen.plugins import BasePlugin

class Plugin(BasePlugin):
    def run(self, source, resource):
        system_meta = etree.Element('system-meta')

        # XXX: could have one resource per output target/format?
        # add some extra meta elements
        system_meta.append(etree.Element('meta', name='srcpath', content=source.srcpath))
        system_meta.append(etree.Element('meta', name='relpath', content=source.relpath))
        system_meta.append(etree.Element('meta', name='srcfile', content=source.srcfile))
        system_meta.append(etree.Element('meta', name='src', content=source.src))
        resource.append(system_meta)

        return resource

