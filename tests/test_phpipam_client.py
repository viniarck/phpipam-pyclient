#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test phpipamclient module
"""

import pytest
from phpipam_pyclient.phpipam_pyclient import PHPIpamClient


class TestPhpIpamClient(object):
    """Class to test PHPIpam Client module"""

    @pytest.fixture(scope='module')
    def get_client(self):
        """PHPIpam client module fixture"""
        return PHPIpamClient()

    @pytest.fixture
    def devices_data(self):
        devices = list()

        # test data
        devices.append({
            'hostname': 'dev1',
            'ip': '1.2.3.4',
            'description': 'Ubuntu'
        })
        devices.append({
            'hostname': 'dev2',
            'ip': '4.3.2.1',
            'description': 'Ubuntu'
        })
        devices.append({
            'hostname': 'dev3',
            'ip': '1.2.3.4',
            'description': 'CentOS'
        })

        return devices

    def test_auth(self, get_client):
        """Test authentication

        """
        client = get_client
        req = client._auth_session()
        assert req.status_code == 200

    def test_add_device(self, get_client, devices_data):
        """Test add devices

        """
        for device in devices_data:
            req = get_client.add_device(device=device)
            assert req == 201

    def test_list_devices(self, get_client, devices_data):
        """Test get all devices

        """
        client = get_client
        resp = client.list_devices()
        # in case devices had been already added (in production or whatever)
        assert len(resp) >= len(devices_data)

    def test_list_devices_filter(self, get_client, devices_data):
        """Test get all devices with filtering

        """
        filter = 'hostname'
        client = get_client
        resp = client.list_devices(fields=[filter])
        for dev in devices_data:
            assert {filter: dev[filter]} in resp

    def test_list_device_fields(self, get_client):
        """Test listing all available fields of devices

        """
        client = get_client
        assert len(client.list_device_fields()) >= 1

    def test_ansible_inv_devices_desc(self, get_client):
        """Test listing unique key values from an endpoint

        """
        client = get_client
        assert client.ansible_inv_endpoint_field('devices/', 'description')

    def test_remove_added_devices(self, get_client, devices_data):
        """Test removing added devices in devices data

        """
        client = get_client
        devs = client.list_devices()
        for dev in devs:
            for ddata in devices_data:
                if dev['hostname'] == ddata['hostname']:
                    req = get_client._delete_device(dev['id'])
                    assert req.status_code == 200
