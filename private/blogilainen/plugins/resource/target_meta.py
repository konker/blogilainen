
import logging
from lxml import etree
from blogilainen.plugins import BasePlugin

class Plugin(BasePlugin):
    def run(self, source, resource):
        target_meta = etree.Element('target-meta')

        for ext,t in source.targets.iteritems():
            target = etree.Element('target', type=ext)

            target.append(etree.Element('meta', name='outpath', content=t.outpath))
            target.append(etree.Element('meta', name='outfile', content=t.outfile))
            target.append(etree.Element('meta', name='ext', content=t.ext))
            target.append(etree.Element('meta', name='out', content=t.out))

            target_meta.append(target)


        resource.append(target_meta)

        return resource


