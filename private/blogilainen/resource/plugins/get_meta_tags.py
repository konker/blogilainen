
import logging
import os
from lxml import etree

from blogilainen.resource.plugins import BasePlugin

AGGREGATE_XSLT_DIR = os.path.join('xslt', 'aggregate')
AGGREGATE_XSLT = os.path.join(AGGREGATE_XSLT_DIR, 'index.xsl')

class Plugin(BasePlugin):
    def meta(self, source, resource):
        transform = etree.XSLT(etree.parse(AGGREGATE_XSLT))

        # execute AGGREGATE_XSLT against src file
        xml = etree.parse(source.src)
        meta = transform(xml).getroot()

        # add to resource
        resource.append(meta)
        return resource

