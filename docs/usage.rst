Usage
=====

phpipam-client leverages python fire to implement the CLI, you can start by checking what options are available:

.. note::

  Before you use this client, the PHPIpam server has to be up and running, since it's going to connect to it.

.. code:: shell

  root@2186b110a223:/app/phpipam_pyclient# python3 phpipam_pyclient.py
  Type:        PHPIpamClient
  String form: <__main__.PHPIpamClient object at 0x7fb28bbf1898>
  Docstring:   PHPIPam Python API Client

  Usage:       phpipam_pyclient.py -
               phpipam_pyclient.py - add-device
               phpipam_pyclient.py - ansible-inv-endpoint-field
               phpipam_pyclient.py - list-device-fields
               phpipam_pyclient.py - list-devices

Since I don't have any devices yet, let me start off by checking the arguments of the add-device function:

- input:

.. code:: shell

  python3 phpipam_pyclient.py - add-device -- --help

- output:

.. code:: shell

  root@f6c8a8161a60:/app/phpipam_pyclient# python3 phpipam_pyclient.py - add-device -- --help
  Type:        method
  String form: <bound method PHPIpamClient.add_device of <__main__.PHPIpamClient object at 0x7fd016505828>>
  File:        phpipam_pyclient.py
  Line:        125
  Docstring:   Adds device to PHPIpam given a dictionary that represents a device
  i.e., it should have these keys at least
  'ip', 'hostname', 'description'

  :device: dictionary that represents a device
  :Returns: REST post status code

  Usage:       phpipam_pyclient.py - add-device [DEVICE]
               phpipam_pyclient.py - add-device [--device DEVICE]
  root@f6c8a8161a60:/app/phpipam_pyclient#

Let's add three devices on PHPIPam:

- input:

.. code:: shell

  python3 phpipam_pyclient.py add-device --device '{hostname:"server1",ip:"1.2.3.4",description:"backend"}'
  python3 phpipam_pyclient.py add-device --device '{hostname:"server2",ip:"1.2.3.5",description:"backend"}'
  python3 phpipam_pyclient.py add-device --device '{hostname:"server3",ip:"1.2.3.6",description:"frontend"}'

- output

Note all REST calls returned 201 (OK) status code:

.. code:: shell

  root@f6c8a8161a60:/app/phpipam_pyclient#   python3 phpipam_pyclient.py add-device --device '{hostname:"server1",ip:"1.2.3.4",description:"backend"}'
  201
  root@f6c8a8161a60:/app/phpipam_pyclient#   python3 phpipam_pyclient.py add-device --device '{hostname:"server2",ip:"1.2.3.5",description:"backend"}'
  201
  root@f6c8a8161a60:/app/phpipam_pyclient#   python3 phpipam_pyclient.py add-device --device '{hostname:"server3",ip:"1.2.3.6",description:"frontend"}'
  201
  root@f6c8a8161a60:/app/phpipam_pyclient#

Now, let's list all devices on PHPIPam:

- input:

.. code:: shell

  python3 phpipam_pyclient.py list-devices

- output:

.. code:: shell

  root@f6c8a8161a60:/app/phpipam_pyclient# python3 phpipam_pyclient.py list-devices
  {"sections": "1;2", "snmp_v3_priv_protocol": "none", "snmp_queries": null, "hostname": "server1", "snmp_port": "161", "rack_size": null, "id": "1", "location": null, "snmp_v3_priv_pass": null, "description": "backend", "snmp_v3_auth_pass": null, "ip": "1.2.3.4", "editDate": null, "snmp_v3_ctx_name": null, "snmp_timeout": "500", "snmp_v3_auth_protocol": "none", "rack_start": null,"snmp_v3_ctx_engine_id": null, "rack": null, "type": "0", "snmp_version": "0", "snmp_community": null, "snmp_v3_sec_level": "none"}
  {"sections": "1;2", "snmp_v3_priv_protocol": "none", "snmp_queries": null, "hostname": "server2", "snmp_port": "161", "rack_size": null, "id": "2", "location": null, "snmp_v3_priv_pass": null, "description": "backend", "snmp_v3_auth_pass": null, "ip": "1.2.3.5", "editDate": null, "snmp_v3_ctx_name": null, "snmp_timeout": "500", "snmp_v3_auth_protocol": "none", "rack_start": null,"snmp_v3_ctx_engine_id": null, "rack": null, "type": "0", "snmp_version": "0", "snmp_community": null, "snmp_v3_sec_level": "none"}
  {"sections": "1;2", "snmp_v3_priv_protocol": "none", "snmp_queries": null, "hostname": "server3", "snmp_port": "161", "rack_size": null, "id": "3", "location": null, "snmp_v3_priv_pass": null, "description": "frontend", "snmp_v3_auth_pass": null, "ip": "1.2.3.6", "editDate": null, "snmp_v3_ctx_name": null, "snmp_timeout": "500", "snmp_v3_auth_protocol": "none", "rack_start": null,"snmp_v3_ctx_engine_id": null, "rack": null, "type": "0", "snmp_version": "0", "snmp_community": null, "snmp_v3_sec_level": "none"}

Sweet! What if I wanted to export these devices as an Ansible inventory? I can group Ansible servers by their description, for example:

- input:

.. code:: shell

  python3 phpipam_pyclient.py ansible-inv-endpoint-field devices/ "description"

.. note::

    Essentially, this command queries the devices/ endpoint and it'll group all hostnames according to their description, you could group by any other attribute if you wanted.

.. code:: shell

  root@f6c8a8161a60:/app/phpipam_pyclient# python3 phpipam_pyclient.py ansible-inv-endpoint-field devices/ "description"
  [frontend]
  server3

  [backend]
  server1
  server2


From this point forward, Ansible all the way to do whatever you need. But, what if you wanted to check all the other available fields what you could filter? If you had custom fields they would show up here too.

- input:

.. code:: shell

  python3 phpipam_pyclient.py list-device-fields

- output:

.. code:: shell

    root@f6c8a8161a60:/app/phpipam_pyclient# python3 phpipam_pyclient.py list-device-fields
  Type:        dict_keys
  String form: dict_keys(['rack_size', 'snmp_v3_priv_pass', 'snmp_community', 'snmp_v3_priv_protocol', 'sections', 'snmp_v3_ctx_name', 'snmp_v3_sec_level', 'editDate', 'rack_start', 'hostname', 'snmp_version', 'snmp_queries', 'snmp_v3_auth_pass', 'snmp_timeout', 'id', 'rack', 'description', 'location', 'snmp_v3_ctx_engine_id', 'ip', 'snmp_v3_auth_protocol', 'type', 'snmp_port'])
  Length:      23

  Usage:       phpipam_pyclient.py list-device-fields
               phpipam_pyclient.py list-device-fields isdisjoint
  root@f6c8a8161a60:/app/phpipam_pyclient#
