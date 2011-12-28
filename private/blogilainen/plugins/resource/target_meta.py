
import os
import re
import logging
from lxml import etree
from blogilainen.plugins import BasePlugin

class Plugin(BasePlugin):
    def run(self, source, resource):
        target_meta = etree.Element('target-meta')

        for ext,t in source.targets.iteritems():
            target = etree.Element('target', type=ext)

            # make sure out path is separated by '/'
            out_path = re.sub(os.sep, '/', t.relative_path)

            target.append(etree.Element('meta', name='out-path', content=out_path))
            target.append(etree.Element('meta', name='basename', content=t.basename))
            target.append(etree.Element('meta', name='ext', content=t.ext))
            target.append(etree.Element('meta', name='out-file', content=t.out_file))
            target.append(etree.Element('meta', name='out', content=t.out_url))

            target_meta.append(target)


        resource.append(target_meta)

        return resource


