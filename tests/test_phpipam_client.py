#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test phpipamclient module
"""

import pytest
import responses
from phpipam_pyclient.phpipam_pyclient import PHPIpamClient


class TestPhpIpamClient(object):
    """Class to test PHPIpam Client module"""

    @pytest.fixture(scope="module")
    def get_client(self):
        """PHPIpam client module fixture"""
        return PHPIpamClient(init_auth=False)

    @pytest.fixture
    def devices_data(self):
        devices = list()

        # test data
        devices.append(
            {
                "hostname": "dev1",
                "ip": "1.2.3.4",
                "description": "Ubuntu",
                "device_type": "server",
                "rack_size": 1,
                "rack_power": "a",
                "id": 1,
            }
        )
        devices.append(
            {
                "hostname": "dev2",
                "ip": "4.3.2.1",
                "description": "Ubuntu",
                "device_type": "server",
                "rack_size": 2,
                "rack_power": 10,
                "id": 2,
            }
        )
        devices.append(
            {
                "hostname": "dev3",
                "ip": "1.2.3.4",
                "description": None,
                "device_type": "server",
                "id": 3,
            }
        )

        return devices

    @responses.activate
    def test_auth(self, get_client):
        """Test authentication"""
        token_res = {"token": "some_token"}
        responses.add(
            responses.POST,
            "http://localhost/api/testing/user/",
            json={"data": token_res},
        )
        client = get_client
        req = client.auth_session()
        assert req.status_code == 200
        assert client._token == token_res

    def test_version(self, get_client):
        """Test version"""
        client = get_client
        assert client.version()

    @responses.activate
    def test_add_device(self, get_client, devices_data):
        """Test add devices"""
        responses.add(
            responses.POST,
            "http://localhost/api/testing/devices/1/",
            json={},
            status=201,
        )
        for device in devices_data:
            req = get_client.add_device(device=device)
            assert req == 201

    @responses.activate
    def test_list_devices(self, get_client, devices_data):
        """Test get all devices"""
        responses.add(
            responses.GET,
            "http://localhost/api/testing/devices/",
            json={"data": devices_data},
        )

        client = get_client
        resp = client.list_devices()
        # in case devices had been already added (in production or whatever)
        assert len(resp) >= len(devices_data)

    @responses.activate
    def test_list_devices_fields(self, get_client, devices_data):
        """Test get all devices with fields selection"""
        responses.add(
            responses.GET,
            "http://localhost/api/testing/devices/",
            json={"data": devices_data},
        )

        client = get_client
        fields = ["hostname"]
        resp = client.list_devices(fields=fields)
        for dev in resp:
            assert list(dev.keys()) == fields

    @responses.activate
    def test_list_devices_filter_eq_contains(self, get_client, devices_data):
        """Test get all devices filter eq and contains"""
        responses.add(
            responses.GET,
            "http://localhost/api/testing/devices/",
            json={"data": devices_data},
        )

        client = get_client
        filters = [
            {"type": "contains", "field": "description", "value": "Ubu"},
            {"type": "eq", "field": "device_type", "value": "server"},
        ]
        resp = client.list_devices(filters=filters)
        for dev in resp:
            assert "Ubu" in dev["description"] and dev["device_type"] == "server"

        filters = [
            {"type": "contains", "field": "description", "value": "not_found"},
        ]
        resp = client.list_devices(filters=filters)
        assert not resp

    @responses.activate
    def test_list_devices_filter_le(self, get_client, devices_data):
        """Test get all devices filter le"""
        responses.add(
            responses.GET,
            "http://localhost/api/testing/devices/",
            json={"data": devices_data},
        )

        client = get_client
        filters = [
            {"type": "le", "field": "rack_size", "value": "3"},
        ]
        resp = client.list_devices(filters=filters)
        assert resp
        for dev in resp:
            assert dev["rack_size"] <= 3

    @responses.activate
    def test_list_devices_filter_lt(self, get_client, devices_data):
        """Test get all devices filter numeric"""
        responses.add(
            responses.GET,
            "http://localhost/api/testing/devices/",
            json={"data": devices_data},
        )

        client = get_client
        filters = [
            {"type": "lt", "field": "rack_size", "value": "2"},
        ]
        resp = client.list_devices(filters=filters)
        assert resp
        for dev in resp:
            assert dev["rack_size"] < 2

    @responses.activate
    def test_list_devices_filter_gt(self, get_client, devices_data):
        """Test get all devices filter gt"""
        responses.add(
            responses.GET,
            "http://localhost/api/testing/devices/",
            json={"data": devices_data},
        )

        client = get_client
        filters = [
            {"type": "gt", "field": "rack_size", "value": "1"},
        ]
        resp = client.list_devices(filters=filters)
        assert resp
        for dev in resp:
            assert dev["rack_size"] > 1

    @responses.activate
    def test_list_devices_filter_ge(self, get_client, devices_data):
        """Test get all devices filter ge"""
        responses.add(
            responses.GET,
            "http://localhost/api/testing/devices/",
            json={"data": devices_data},
        )

        client = get_client
        filters = [
            {"type": "ge", "field": "rack_size", "value": "1"},
        ]
        resp = client.list_devices(filters=filters)
        assert resp
        for dev in resp:
            assert dev["rack_size"] >= 1

    @responses.activate
    def test_list_device_fields(self, get_client, devices_data):
        """Test listing all available fields of devices"""
        responses.add(
            responses.GET,
            "http://localhost/api/testing/devices/",
            json={"data": devices_data},
        )

        client = get_client
        assert len(client.list_device_fields()) >= 1

    @responses.activate
    def test_ansible_inv_devices_desc(self, get_client, devices_data):
        """Test listing unique key values from an endpoint"""
        responses.add(
            responses.GET,
            "http://localhost/api/testing/devices/",
            json={"data": devices_data},
        )

        client = get_client
        assert client.ansible_inv_endpoint_field("devices/", "description")

    @responses.activate
    def test_remove_added_devices(self, get_client, devices_data):
        """Test removing added devices in devices data"""
        responses.add(
            responses.GET,
            "http://localhost/api/testing/devices/",
            json={"data": devices_data},
        )
        for i in range(1, 4):
            responses.add(
                responses.DELETE, f"http://localhost/api/testing/devices/{i}/", json={}
            )

        client = get_client
        devs = client.list_devices()
        for dev in devs:
            for ddata in devices_data:
                if dev["hostname"] == ddata["hostname"]:
                    req = get_client._delete_device(dev["id"])
                    assert req.status_code == 200

    @responses.activate
    def test_list_devices_filter_ge_float_cast(self, get_client, devices_data):
        """Test get all devices filter ge with float cast"""
        responses.add(
            responses.GET,
            "http://localhost/api/testing/devices/",
            json={"data": devices_data},
        )

        client = get_client
        filters = [
            {"type": "ge", "field": "rack_power", "value": "1"},
        ]
        resp = client.list_devices(filters=filters)
        assert resp
        for dev in resp:
            if "rack_size" in dev:
                assert dev["rack_size"] >= 1
