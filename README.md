# dsv-ansible
Custom ansible modules for DSV

## dsv_inventory.py
An inventory plugin that allows a "reverse" handling of host groups compared to the standard ansible approach.

Each host is defined at the top level of the (YAML-formatted) inventory file, with its groups listed beneath. Any items in the list that are mappings are treated as host variables instead of groups.

Example:
```
example-host:
 - east-datacenter
 - db
 - proxy_host: myproxy

other-host:
 - east-datacenter
 - public
 - loadbalancer
```
