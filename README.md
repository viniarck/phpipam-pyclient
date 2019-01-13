[![pipeline status](https://gitlab.com/viniarck/phpipam-pyclient/badges/master/pipeline.svg)](https://gitlab.com/viniarck/phpipam-pyclient/commits/master) [![Documentation Status](https://readthedocs.org/projects/phpipam-pyclient/badge/?version=latest)](http://phpipam-pyclient.readthedocs.io/en/latest/?badge=latest)

## phpipam-pyclient

![logo](https://lh3.googleusercontent.com/eHiLUXP1dqG1E-iuPP2T6AjXaID_Sf5ivjBl8JHguGBpjJUl9fXSX8oGh2giCy6ICsgCXOi_kUeTHK9G_IFQtU46MDgwh-E9xupJnnfZg_wQdbk19_DuqaAPd9C2fbv6KaiR6wX1rocHpwYddZZPVRz_MehgJd7Xq7oMvFDk8hMWsw4t7IDcVWqecYq0qvJ_J0y3I5_IN_N3LqaO9dw-aU5jlmQaKGcqUIX3CzPT0LrXjisvZW3NS6O0sDKPGP7ZiDxK4NmeHgAPtHrCWieqGRLMx76mnn_Myc5a7Cild9TuteAKGgcsNZYAxMMeLz79pokAxQBGuvaOPYWFe7QS7cG098XukqXVLz8alnNxAaqGkPt_i2IYH2ENEVfa7CZmUjPvA2WvsnWypm2dfq1YRH2jc0zZWT2v2TZD7xKn8REX7EmXYPtYWjeRLQBA1duHA6R6BO1DPkBfAQAfcmsYnSIjxiyIieNem6k6iNlOt1ww61_r4cMcQXX8zmwYAIzUObOskU6e17kUBh2Yy1jyI5Lab0LKJ9TDJ-G_FgWtWe9J_X6gvxI5P4cWREoRoWvagTDI_uPCH0NNv5GUrYAtuCKa8tKb88OzrEZGxgzvUbO0TkEYpHOTizUUyhvRimfosMUMzuQOXQMW2R_yc7qKLRc=w400-h150-no)

phpipam-pyclient is a REST-client CLI tool to interface with [phpipam](https://github.com/phpipam/phpipam) REST API. phpipam-pyclient leverages python fire and requests under the hood, some high level functions have been implemented to allow the user to quickly query certain information about the devices on phpipam. In addition, you can use this library to build your Ansible inventory by filtering a field/column of the devices on phpipam.

### Testing

Integration tests are implemented with pytest validating both Python3.6 and Python2.7 on a docker-based environment, in two stages:

- installation: validates a phpipam installation from strach with selenium.
- client-server API: validates phpipam-pyclient with phpipam REST client.

The following versions of phpipam are being tested on GitLab CI:

- 1.3.2 (latest as of now)
- 1.3.1
- 1.3

## Installation

You have two options, either via the source code on Github or Docker. After completing the installation, you have to configure the parameters to authenticate your user on phpipam in the ``phpipam_pyclient/config.json`` file. You can find more information, examples and usage on [ReadTheDocs](http://phpipam-pyclient.readthedocs.io/).

### via GitHub

```
git clone https://github.com/viniarck/phpipam-pyclient.git
cd phpipam-pyclient
pip install -e .
```

### Docker

```
docker run -i -t -d --name phpipam-pyclient registry.gitlab.com/viniarck/phpipam-pyclient:dev
```

```
docker exec -i -t phpipam-pyclient /bin/bash -c 'phpipam-pyclient'
```

## Changelog

[CHANGELOG.md](./CHANGELOG.md)
