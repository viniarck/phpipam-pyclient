Installation
============

You have two options, either via the source code on Github or Docker:

via Github
----------

1 - Git clone

::

  git clone https://github.com/viniciusarcanjo/phpipam-python-client.git; cd phpipam-pyclient

2 - Install Python requirements dependencies, either via user install or virtualenv:

2.1 - pip user install:

::

  pip3 install -r requirements.txt --user

2\.1 - or virtualenv:

::

  virtualenv -p python3.5 .venv
  source .venv/bin/activate
  pip3 install -r requirements.txt

via Docker
----------

::

  docker pull registry.gitlab.com/viniciusarcanjo/phpipam-python-client:dev
