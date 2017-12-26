Introduction
============

phpipam-pyclient is a REST-client CLI tool to interface with PHPIpam REST API. phpipam-pyclient leverages python fire and requests under the hood, some high level functions have been implementend to allow the user to quickly query certain information about the devices on PHPIpam. In addition, you can use this library to build your Ansible inventory by filtering a field/column of the devices on PHPIpam.

Testing
-------

Integration tests are implemented with pytest validating both Python2.7 and Python3.5 on a docker-based environment, in two stages:

- installation: validates a installation from strach with selenium.
- client-server API: validates this phpipam-pyclient with the phpipam REST API.

The following versions of PHPIpam are being tested on GitLab CI:

- 1.3.1
- 1.3
