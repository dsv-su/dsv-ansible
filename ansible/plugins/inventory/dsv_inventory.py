#!/usr/bin/python

from ansible.plugins.inventory import BaseInventoryPlugin
try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping

EXAMPLES = '''
server1:
 - group1
 - group2
 - host-var1: value
 - host-var2: othervalue

server2:
 - group1
 - group3
 - host-var2: thirdvalue
'''

NAME = 'dsv_inventory'

class InventoryModule(BaseInventoryPlugin):
    NAME = 'dsv_inventory'

    def __init__(self):
        super(InventoryModule, self).__init__()

    def verify_file(self, path):
        if not super(InventoryModule, self).verify_file(path):
            return False
        return True

    def parse(self, inventory, loader, path, cache=False):
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        try:
            data = self.loader.load_from_file(path, cache=False)
        except Exception as e:
            raise AnsibleParserError(e)
        if not data:
            raise AnsibleParserError('Parsed empty YAML file')
        if not isinstance(data, MutableMapping):
            raise AnsibleParserError('YAML inventory has invalid structure, it should be a dictionary, got: %s' % type(data))

        for host in data:
            self._parse_host(host, data[host])

    def _parse_host(self, host, hostdata):
        self.inventory.add_host(host)
        for item in hostdata:
            if isinstance(item, MutableMapping):
                hostvars = item
                for var in hostvars:
                    self.inventory.set_variable(host, var, hostvars[var])
            else:
                group = item
                self.inventory.add_group(group)
                self.inventory.add_host(host, group)
                
