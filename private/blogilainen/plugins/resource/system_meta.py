
import logging
from lxml import etree
from blogilainen.plugins import BasePlugin

class Plugin(BasePlugin):
    def run(self, source, resource):
        sys_meta = etree.Element('sys-meta')

        # XXX: could have one resource per output target/format?
        # add some extra meta elements
        sys_meta.append(etree.Element('meta', name='srcpath', content=source.srcpath))
        sys_meta.append(etree.Element('meta', name='relpath', content=source.relpath))
        sys_meta.append(etree.Element('meta', name='srcfile', content=source.srcfile))
        sys_meta.append(etree.Element('meta', name='src', content=source.src))
        resource.append(sys_meta)

        return resource

