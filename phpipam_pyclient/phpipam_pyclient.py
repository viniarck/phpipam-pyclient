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
from collections import defaultdict
from phpipam_pyclient.version import __version__

DISABLE_SSL_WARNINGS = True
if DISABLE_SSL_WARNINGS:
    warnings.filterwarnings("ignore")


class PHPIpamClient(object):
    """PHPIPam Python API Client"""

    def __init__(self, cfg_file="config.json", init_auth=True):
        """PHPIpam Python client
        This class is meant to be used with Google's fire in order to also
        be used in a CLI exploring style.
        """
        try:
            self.load_config(cfg_file=cfg_file)
            self._token = None
            self._session = None
            self._verify = False
            if init_auth:
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

    def load_config(self, cfg_file="config.json"):
        """Load configuration file specified in config.json

        If the PHPIPAM_PYCLIENT_CFG_FILE environment variable
        exists, it takes higher precedence.

        :cfg_file: configuration file

        """
        file_path = os.environ.get("PHPIPAM_PYCLIENT_CFG_FILE")
        if not file_path:
            file_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)), cfg_file
            )
        with open(file_path) as json_file:
            data = json.load(json_file)
            self._base_url = data["base_url"]
            self._api_name = data["api_name"]
            self._auth_url = "{0}/{1}/user/".format(self._base_url, self._api_name)
            self._api_url = "{0}/{1}".format(self._base_url, self._api_name)
            self._user = data["user"]
            self._passwd = data["passwd"]

    def _build_url(self, endpoint: str):
        """Build url"""
        return f"{self._api_url}/{endpoint}"

    def auth_session(self):
        """Authenticate on PHPIpam API"""
        req = requests.post(
            self._auth_url, auth=(self._user, self._passwd), verify=self._verify
        )
        if req.status_code != 200:
            raise requests.exceptions.RequestException(
                "Authentication failed on {0}".format(self._auth_url)
            )
        self._token = {"token": req.json()["data"]["token"]}
        return req

    def list_device_fields(self):
        """List all devices' available fields/columns"""
        req = requests.get(
            self._build_url("devices/"), headers=self._token, verify=self._verify
        )
        req.raise_for_status()
        data = req.json()["data"]
        for device in data:
            return list(device.keys())
        return []

    def _validate_ansible_kwargs(self, dict_value):
        if not isinstance(dict_value, dict):
            raise ValueError(
                f"ansible_kwargs is supposed to be a dict. got {dict_value}"
            )
        for key in dict_value.keys():
            if not isinstance(dict_value[key], dict):
                raise ValueError(f"ansible_kwargs key '{key}' is supposed to be a dict")
        return dict_value

    def ansible_inv_endpoint_field(
        self, endpoint, group_field, include_groups=[], filters=[], ansible_kwargs={}
    ):
        """Group devices based on a unique field value and outputs
        Ansible inventory

        :endpoint: endpoint to be filtered, e.g., devices/
        :group_field: field to be filtered as a group, e.g., "description",
        :include_groups: ansible groups to be included, if empty, includes all
        :filters: filter objects to filter each host field with an expression and value
        :ansible_kwargs: ansible kwargs to be set based on a group name as default values
        :Returns: str formated as Ansible inventory

        Example:
        - endpoint=devices/
        - group_field=description
        - include_groups=["backend"]
        - filters=[{"type": "contains", "field": "hostname", "value": "light"}]
        - ansible_kwargs={"backend": {"ansible_port": "2222"}}
        """
        try:
            self._validate_ansible_kwargs(ansible_kwargs)
        except ValueError as e:
            print(str(e))
            sys.exit(1)

        req = requests.get(
            self._build_url(endpoint), headers=self._token, verify=self._verify
        )
        req.raise_for_status()
        data = req.json().get("data")
        if not data:
            return None

        device_list = data
        for filter_obj in filters:
            try:
                device_list = self._apply_filter(filter_obj, device_list)
            except ValueError as e:
                print(str(e))
                sys.exit(1)

        dev = defaultdict(list)
        for device in device_list:
            if not device.get(group_field):
                continue
            if include_groups and device.get(group_field) not in include_groups:
                continue
            dev[device.get(group_field)].append(device.get("hostname"))

        res = str()
        for key, value in dev.items():
            res = res + "[{0}]\n".format(key)
            for host in value:
                if key not in ansible_kwargs:
                    res = res + "{0}\n".format(host)
                else:
                    args = [f"{k}={v}" for k, v in ansible_kwargs[key].items()]
                    res = res + "{0} {1}\n".format(host, " ".join(args))
            res = res + "\n"
        return res

    def _delete_device(self, id):
        """Delete a device given a database id"""
        url = "{0}/{1}".format(self._api_url, "devices/{0}/".format(id))
        return requests.delete(url, headers=self._token, verify=self._verify)

    def add_device(self, device=None):
        """Add device to PHPIpam given a dictionary that represents a device
        i.e., it should have these keys at least
        'ip', 'hostname', 'description'

        :device: dictionary that represents a device
        :Returns: REST post status code

        """
        if isinstance(device, str):
            device = json.loads(device)
        url = f"{self._api_url}/devices/1/"
        return requests.post(
            url, headers=self._token, verify=self._verify, data=device
        ).status_code

    def _apply_filter(self, filter_obj, collection):
        """Apply a filter to a collection"""
        if not collection:
            return collection

        if not isinstance(filter_obj, dict):
            raise ValueError(f"filter {filter_obj} must be a dictionary")
        if any(
            (
                "type" not in filter_obj,
                "field" not in filter_obj,
                "value" not in filter_obj,
            )
        ):
            raise ValueError(
                f"filter must have 'type', 'field' and 'value' keys. obj: {filter_obj}"
            )

        def float_cast(value) -> float:
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0

        filter_value = filter_obj["value"]
        filter_field = filter_obj["field"]
        filter_types = {
            "contains": lambda x: filter_value in str(x.get(filter_field)),
            "eq": lambda x: filter_value == str(x.get(filter_field)),
            "ge": lambda x: float(filter_value) <= float_cast(x.get(filter_field)),
            "gt": lambda x: float(filter_value) < float_cast(x.get(filter_field)),
            "le": lambda x: float(filter_value) >= float_cast(x.get(filter_field)),
            "lt": lambda x: float(filter_value) > float_cast(x.get(filter_field)),
        }
        if filter_obj["type"] not in filter_types:
            raise ValueError(
                f"invalid filter type, it must be of one these values: {list(filter_types.keys())}"
            )

        return list(
            filter(
                filter_types[filter_obj["type"]],
                [elem for elem in collection if filter_obj["field"] in elem],
            )
        )

    def list_devices(self, fields=None, filters=[]):
        """List all devices and filter for specific fields

        :fields: optional field attributes to be included, includes all by default
        :filters: filter objects to filter each field with an expression and value

        Example:
        - fields=["ip", "hostname", "vendor"]
        - filters=[{"type": "contains", "field": "hostname", "value": "light"}]

        """
        if not isinstance(fields, list):
            fields = []

        req = requests.get(
            self._build_url("devices/"), headers=self._token, verify=self._verify
        )
        req.raise_for_status()

        data = req.json().get("data")
        if not data:
            return []

        device_list = []
        for device in data:
            if not fields:
                device_list.append(device)
                continue

            dev = {}
            for field in fields:
                dev[field] = device.get(field)
            if dev:
                device_list.append(dev)

        try:
            for filter_obj in filters:
                device_list = self._apply_filter(filter_obj, device_list)
            return device_list
        except ValueError as e:
            print(str(e))
            sys.exit(1)

    def version(self):
        """Get phpipam-pyclient version."""
        return __version__


def main():
    fire.Fire(PHPIpamClient)


if __name__ == "__main__":
    main()
