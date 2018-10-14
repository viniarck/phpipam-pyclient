## phpipam-pyclient

phpipam-pyclient is a REST-client CLI tool to interface with [phpipam](https://github.com/phpipam/phpipam) REST API. phpipam-pyclient leverages python fire and requests under the hood, some high level functions have been implementend to allow the user to quickly query certain information about the devices on phpipam. In addition, you can use this library to build your Ansible inventory by filtering a field/column of the devices on phpipam.

### Testing

[![pipeline status](https://gitlab.com/viniarck/phpipam-pyclient/badges/master/pipeline.svg)](https://gitlab.com/viniarck/phpipam-pyclient/commits/master)

Integration tests are implemented with pytest validating both Python3.6 and Python2.7 on a docker-based environment, in two stages:

- installation: validates a phpipam installation from strach with selenium.
- client-server API: validates this phpipam-pyclient with phpipam REST API.

The following versions of phpipam are being tested on GitLab CI:

- 1.3.2 (latest as of now)
- 1.3.1
- 1.3

## Installation

You have two options, either via the source code on Github or Docker:

### via Github

1 - Git clone

```
git clone https://github.com/viniarck/phpipam-python-client.git; cd phpipam-pyclient
```

2 - Install Python requirements dependencies, either via user install or virtualenv:

2.1 - pip user install:

```
pip3 install -r requirements.txt --user
```

2\.1 - or virtualenv:

```
virtualenv -p python3.6 .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

### With Docker container

```
docker run -i -t -d --name phpipam-pyclient registry.gitlab.com/viniarck/phpipam-pyclient:dev
```

Edit your config.json file, either mount or copy to the container:

```
docker cp ./phpipam_pyclient/config.json phpipam-pyclient:/app/phpipam_pyclient/
```

Run the application:

```
docker exec -i -t phpipam-pyclient /bin/bash -c 'cd phpipam_pyclient; python3 phpipam_pyclient.py'
```

## Docs

[![Documentation Status](https://readthedocs.org/projects/phpipam-pyclient/badge/?version=latest)](http://phpipam-pyclient.readthedocs.io/en/latest/?badge=latest)

After completing the installation, you have to configure the parameters to authenticate your user on phpipam in the ``phpipam_pyclient/config.json`` file. You can find more information, examples and usage on [ReadTheDocs](http://phpipam-pyclient.readthedocs.io/).
