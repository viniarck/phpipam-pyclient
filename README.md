[![pipeline status](https://gitlab.com/viniarck/phpipam-pyclient/badges/master/pipeline.svg)](https://gitlab.com/viniarck/phpipam-pyclient/commits/master) [![Documentation Status](https://readthedocs.org/projects/phpipam-pyclient/badge/?version=latest)](http://phpipam-pyclient.readthedocs.io/en/latest/?badge=latest)

## phpipam-pyclient

![logo](./images/phpipampyclient.png)

phpipam-pyclient is a REST-client CLI tool to interface with [phpipam](https://github.com/phpipam/phpipam) REST API. phpipam-pyclient leverages python fire and requests under the hood, some high level functions have been implemented to allow the user to quickly query certain information about the devices on phpipam. In addition, you can use this library to build your Ansible inventory by filtering a field/column of the devices on phpipam.

## Installation

Currently, the only supported installation is directly via checking the code from GitHub. After completing the installation, you have to configure the parameters to authenticate your user on phpipam in the ``phpipam_pyclient/config.json`` file. You can find more information, examples and usage on [ReadTheDocs](http://phpipam-pyclient.readthedocs.io/).

### via GitHub

```
git clone https://github.com/viniarck/phpipam-pyclient.git
cd phpipam-pyclient
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -e .
```

## Changelog

[CHANGELOG.md](./CHANGELOG.md)
