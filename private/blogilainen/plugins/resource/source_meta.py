
import logging
import os
from lxml import etree

from blogilainen.plugins import BasePlugin

class Plugin(BasePlugin):
    def run(self, source, resource):
        get_meta = etree.XPath("//meta")
        source_meta = etree.Element('source-meta')

        xml = etree.parse(source.src)
        metas = get_meta(xml)
        for m in metas:
            source_meta.append(m)

        # add to resource
        resource.append(source_meta)

        return resource

