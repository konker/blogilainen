
import logging
from lxml import etree
from blogilainen.plugins import BasePlugin

class Plugin(BasePlugin):
    def run(self, source, resource):
        target_meta = etree.Element('target-meta')

        for ext,t in source.targets.iteritems():
            target = etree.Element('target', type=ext)

            target.append(etree.Element('meta', name='physical-path', content=t.physical_path))
            target.append(etree.Element('meta', name='virtual-path', content=t.virtual_path))
            target.append(etree.Element('meta', name='out-file', content=t.out_file))
            target.append(etree.Element('meta', name='ext', content=t.ext))
            target.append(etree.Element('meta', name='out', content=t.out))

            target_meta.append(target)


        resource.append(target_meta)

        return resource


