#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PHPIpam Python API Client
"""

import fire
import json
import warnings
import requests
import os
import sys
from phpipam_pyclient.version import __version__
DISABLE_SSL_WARNINGS = True
if DISABLE_SSL_WARNINGS:
    warnings.filterwarnings("ignore")


class PHPIpamClient(object):
    """PHPIPam Python API Client"""

    def __init__(self, cfg_file='config.json', open_con=True, load_conf=True):
        """PPHIpam Python client
        This class is meant to be used with Google's fire in order to also
        be used in a CLI exploring style.

        :cfg_file: json configuration file
        :open_con: True to open TCP connection
        :open_con: True to auto load config

        """
        try:
            self.load_config(cfg_file=cfg_file)
            self._token = None
            self._session = None
            self._verify = False
            if open_con:
                self.auth_session()
        except FileNotFoundError as e:
            print(str(e))
        except json.JSONDecodeError as e:
            print(str(e))
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(str(e))
            print("\nHave you configured your config.json file yet? ")
            sys.exit(1)

    def load_config(self, cfg_file='config.json'):
        """Load configuration file specified in config.json

        If the PHPIPAM_PYCLIENT_CFG_FILE environment variable
        exists, it takes higher precedence.

        :cfg_file: configuration file

        """
        file_path = os.environ.get("PHPIPAM_PYCLIENT_CFG_FILE")
        if not file_path:
            file_path = os.path.join(os.path.abspath(
                                     os.path.dirname(__file__)),
                                     cfg_file)
        with open(file_path) as json_file:
            data = json.load(json_file)
            self._base_url = data['base_url']
            self._api_name = data['api_name']
            self._auth_url = "{0}/{1}/user/".format(self._base_url,
                                                    self._api_name)
            self._api_url = "{0}/{1}".format(self._base_url, self._api_name)
            self._user = data['user']
            self._passwd = data['passwd']

    def auth_session(self):
        """Authenticate on PHPIpam API

        """
        req = requests.post(self._auth_url, auth=(self._user, self._passwd),
                            verify=self._verify)
        if req.status_code != 200:
            raise requests.exceptions.RequestException(
                "Authentication failed on {0}".format(self._auth_url))
        self._token = {"token": req.json()['data']['token']}
        return req

    def _call(self, endpoint):
        """Generic requests an endpoint based on API url's

        """
        url = "{0}/{1}".format(self._api_url, endpoint)
        return requests.get(url, headers=self._token, verify=self._verify)

    def _post(self, endpoint, data):
        """Generic posts to an endpoint based on API url's

        """
        url = "{0}/{1}".format(self._api_url, endpoint)
        return requests.post(
            url, headers=self._token, verify=self._verify, data=data)

    def list_device_fields(self):
        """List all devices' available fields/columns

        """
        req = self._call(endpoint='devices/')
        if req.status_code == 200:
            data = req.json()['data']
            for device in data:
                return device.keys()
        return []

    def ansible_inv_endpoint_field(self, endpoint, field):
        """Group devices based on a unique field value and outputs
        Ansible inventory

        :endpoint: endpoint to be filtered, e.g., devices/
        :field: field to be filtered as a group, e.g., "description",
        "server_os" (custom), etc..
        :Returns: str formated as Ansible inventory

        """
        req = self._call(endpoint=endpoint)
        if req.status_code == 200:
            data = req.json().get('data')
            if data:
                dev = {}
                for device in data:
                    if device.get(field):
                        if dev.get(device.get(field)):
                            dev[device.get(field)].append(
                                device.get('hostname'))
                        else:
                            dev[device.get(field)] = [(device.get('hostname'))]
                res = str()
                for key, value in dev.items():
                    res = res + "[{0}]\n".format(key)
                    for host in value:
                        res = res + "{0}\n".format(host)
                    res = res + "\n"
                return res
        return None

    def _delete_device(self, id):
        """Delete a device given a database id

        """
        url = "{0}/{1}".format(self._api_url, 'devices/{0}/'.format(id))
        return requests.delete(url, headers=self._token, verify=self._verify)

    def add_device(self, device=None):
        """Add device to PHPIpam given a dictionary that represents a device
        i.e., it should have these keys at least
        'ip', 'hostname', 'description'

        :device: dictionary that represents a device
        :Returns: REST post status code

        """
        # in order to pass a dict via CLI
        if isinstance(device, str):
            device = json.loads(device)
        return self._post(endpoint='devices/1/', data=device).status_code

    def list_devices(self, fields=None):
        """List all devices and filter for specific fields

        :fields: optional field attributes to be filtered

        Example:
        - fields=["ip", "hostname"]

        """
        if not isinstance(fields, list):
            fields = []
        req = self._call(endpoint='devices/')
        if req.status_code == 200:
            device_list = []
            data = req.json().get('data')
            # it can be None type.
            if data:
                for device in data:
                    if fields:
                        dev = {}
                        for field in fields:
                            dev[field] = device.get(field)
                        if dev:
                            device_list.append(dev)
                    else:
                        device_list.append(device)
            return device_list

    def version(self):
        """Get phpipam-pyclient version."""
        return __version__


def main():
    fire.Fire(PHPIpamClient)


if __name__ == "__main__":
    main()
