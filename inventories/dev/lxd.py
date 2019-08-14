#!/usr/bin/env python

# (c) 2013, Michael Scherer <misc@zarb.org>
# (c) 2014, Hiroaki Nakamura <hnakamur@gmail.com>
# (c) 2016, Andew Clarke <andrew@oscailte.org>
#
# This file is based on https://github.com/ansible/ansible/blob/devel/plugins/inventory/libvirt_lxc.py which is part of Ansible,
# and https://github.com/hnakamur/lxc-ansible-playbooks/blob/master/provisioning/inventory-lxc.py
#
# NOTE, this file has some obvious limitations, improvements welcome
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import os
from subprocess import Popen, PIPE
import distutils.spawn
import sys
import json
import re
from pprint import pprint

from ansible.module_utils.six.moves import configparser

# Set up defaults
resource = 'local:'
available_groups = {'master', 'workers'}
connection = 'lxd'
hosts = {}
result = {}



# Read the settings from the lxd.ini file
config = configparser.SafeConfigParser()

config.read(os.path.dirname(os.path.realpath(__file__)) + '/lxd.ini')
#if config.has_option('lxd', 'resource'):
    #resource = config.get('lxd', 'resource')
#if config.has_option('lxd', 'group'):
    #group = config.get('lxd', 'group')
if config.has_option('lxd', 'connection'):
    connection = config.get('lxd', 'connection')

regex = re.compile('^.*-.*-(.*)-.*$')

# Ensure executable exists
if distutils.spawn.find_executable('lxc'):

    # Set up containers result and hosts array
    for group in available_groups:
        result[group] = {}
        result[group]['hosts'] = []
        result[group]['vars'] = {} 
        result[group]['vars']['ansible_connection'] = connection

    # Run the command and load json result
    pipe = Popen(['lxc', 'list', resource, '--format', 'json'], stdout=PIPE, universal_newlines=True)
    lxdjson = json.load(pipe.stdout)
    # print(json.dumps(lxdjson))

    # Iterate the json lxd output
    for item in lxdjson:
        
        # Check state and network
        if 'state' in item and item['state'] is not None and 'network' in item['state']:
            network = item['state']['network']

            # Check for eth0 and addresses
            if 'eth0' in network and 'addresses' in network['eth0']:
                addresses = network['eth0']['addresses']

                # Iterate addresses
                for address in addresses:

                    # Only return inet family addresses
                    if 'family' in address and address['family'] == 'inet':
                        if 'address' in address:
                            ip = address['address']
                            real_name = item['name']
                            x = regex.match(real_name)

                            name = x.group(1)
                            # Add the host to the results and the host array

                            group_name = 'workers'
                            if name.find('master') >= 0:
                                group_name = 'master'
                            
                            
                            result[group_name]['hosts'].append(name)
                            result[group_name]['vars']['ansible_ssh_user'] = "vagrant"
                            result[group_name]['vars']['ansible_ssh_host'] = "local:"+real_name
                            #hosts[name] = ip

    # Set the other containers result values
    # result['lxd']['vars'] = {}
    # result['lxd']['vars']['ansible_connection'] = connection

# Process arguments
if len(sys.argv) == 2 and sys.argv[1] == '--list':
    print(json.dumps(result))
elif len(sys.argv) == 3 and sys.argv[1] == '--host':
    if sys.argv[2] == 'localhost':
        print(json.dumps({'ansible_connection': 'local'}))
    else:
        if connection == 'lxd':
            print(json.dumps({'ansible_connection': connection}))
        else:
            print(json.dumps({'ansible_ssh_user': 'vagrant', 'ansible_connection': connection, 'ansible_host': hosts[sys.argv[2]]}))
else:
    print("Need an argument, either --list or --host <host>")
