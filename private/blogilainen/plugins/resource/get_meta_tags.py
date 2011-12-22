
import logging
import os
from lxml import etree

from blogilainen.plugins import BasePlugin

class Plugin(BasePlugin):
    def run(self, source, resource):
        get_meta = etree.XPath("//meta")
        src_meta = etree.Element('src-meta')

        xml = etree.parse(source.src)
        metas = get_meta(xml)
        for m in metas:
            src_meta.append(m)

        # add to resource
        resource.append(src_meta)

        return resource

