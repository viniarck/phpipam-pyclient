Installation
============

You have two options, either via the source code on Github or Docker:

via Github
----------

1 - Git clone

::

  git clone https://github.com/viniarck/phpipam-pyclient.git; cd phpipam-pyclient

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

  docker run -i -t -d --name phpipam-pyclient viniarck/phpipam-pyclient:dev

Edit your config.json file, either mount or copy to the container:

::

  docker cp <config.json> phpipam-pyclient:/app/phpipam_pyclient/

Run the application:

::

  docker exec -i -t phpipam-pyclient /bin/bash -c 'cd phpipam_pyclient; python3 phpipam_pyclient.py'
