
import logging
from lxml import etree
from blogilainen.plugins import BasePlugin

class Plugin(BasePlugin):
    def run(self, source, resource):
        system_meta = etree.Element('system-meta')

        # XXX: could have one resource per output target/format?
        # add some extra meta elements
        #system_meta.append(etree.Element('meta', name='source-path', content=source.source_path))
        system_meta.append(etree.Element('meta', name='source-path', content=source.relative_path))
        system_meta.append(etree.Element('meta', name='basename', content=source.basename))
        system_meta.append(etree.Element('meta', name='ext', content=source.ext))
        system_meta.append(etree.Element('meta', name='source-file', content=source.source_file))
        system_meta.append(etree.Element('meta', name='source', content=source.source_url))
        #system_meta.append(etree.Element('meta', name='source', content=source.source))
        resource.append(system_meta)

        return resource

