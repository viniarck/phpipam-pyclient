#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import socket
import pytest
import time


class TestPhpIpamInstallation(object):
    """Integration tests for PHPIpam API Installation from scratch"""

    @pytest.fixture
    def get_args(self):
        """Get module args, selenium drivers and URLs
        :returns: TODO

        """
        args = dict()
        options = webdriver.ChromeOptions()
        URL = 'http://selenium:4444/wd/hub'
        # options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--screen-size=1920x1080")

        drv = webdriver.Remote(
            command_executor=URL,
            desired_capabilities=options.to_capabilities())

        drv.implicitly_wait(5)
        # selenium driver
        args['drv'] = drv
        # db and web host according to docker compose
        web_host = 'ipam'
        db_host = 'mysql'
        web_port = 80
        db_port = 3306
        args['db_host'] = db_host
        args['db_port'] = db_port
        args['web_host'] = web_host
        args['web_port'] = web_port
        # URLs
        main_url = 'http://{0}:{1}/?page=install&section=install_automatic'
        login_url = 'http://{0}:{1}/?page=login'
        settings_url = 'http://{0}:{1}/?page=administration&section=settings'
        settings_api_url = 'http://{0}:{1}/?page=administration&section=api'
        args['main_url'] = main_url.format(web_host, web_port)
        args['login_url'] = login_url.format(web_host, web_port)
        args['settings_url'] = settings_url.format(web_host, web_port)
        args['settings_api_url'] = settings_api_url.format(web_host, web_port)
        args['app_name'] = 'testing'
        # generic password
        args['pw'] = 'my-secret-pw'

        return args

    @pytest.fixture
    def find_element_dict_send_keys(self, function, payload):
        """Generic function to find an element given a function and payload dict

        :function: selenium find_element_by_*
        :payload: dictionary payload, field and values

        """
        for key, value in payload.items():
            function(key).send_keys(value)

    def try_to_login(self, drv_dict):
        """Function to login

        """
        drv = drv_dict['drv']
        pw = drv_dict['pw']
        # login
        drv.get(drv_dict['login_url'])
        try:
            payload = {'ipamusername': 'admin', 'ipampassword': pw}
            self.find_element_dict_send_keys(drv.find_element_by_name, payload)
            drv.find_element_by_xpath(
                '//*[@id="login"]/div/div[6]/input').click()
        except NoSuchElementException:
            # It's already auth.
            pass

    def test_tcp_connections(self, get_args):
        """Test TCP connection to PHPIpam and database

        """
        db_host = get_args['db_host']
        db_port = get_args['db_port']
        web_host = get_args['web_host']
        web_port = get_args['web_port']

        max_attemps = 10
        wait_for = 1
        servers = [(web_host, web_port), (db_host, db_port)]
        for retry in range(0, max_attemps):
            for server in servers:
                soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                soc.settimeout(2)
                res = soc.connect_ex((server[0], server[1]))
                if res != 0:
                    break
                else:
                    assert True
                    return
            time.sleep(wait_for)
        assert False

    def test_fresh_install(self, get_args):
        """Test a fresh new install

        """
        drv = get_args['drv']
        pw = get_args['pw']
        drv.get(get_args['main_url'])

        # first screen
        payload = {'mysqlrootuser': 'root', 'mysqlrootpass': pw}
        self.find_element_dict_send_keys(drv.find_element_by_name, payload)

        # In case the db refuses connection.
        max_retries = 5
        succeeded = False
        for _ in range(0, max_retries):
            try:
                drv.find_element_by_partial_link_text('Install').click()
                drv.find_element_by_partial_link_text('Continue').click()
                succeeded = True
                break
            except NoSuchElementException:
                pass
        if not succeeded:
            assert False

        # second screen
        payload = {'password1': pw, 'password2': pw, 'siteURL': 'phpipam'}
        self.find_element_dict_send_keys(drv.find_element_by_name, payload)
        drv.find_element_by_xpath(
            '//*[@id="postinstall"]/div/div[10]/div/input').click()
        # success message.
        drv.find_element_by_partial_link_text('Proceed').click()

    def test_enable_api(self, get_args):
        """Test login and enable the API

        """
        drv = get_args['drv']
        self.try_to_login(get_args)
        for _ in range(0, 2):
            drv.get(get_args['settings_url'])
        # scroll down to click API button
        drv.execute_script("window.scrollTo(0, 800);")
        try:
            drv.find_element_by_xpath(
                '//*[@id="settings"]/tbody/tr[16]/td[2]/div/div/span[2]'
                ).click()
        except NoSuchElementException:
            # new version has changed the layout slightly
            drv.find_element_by_xpath(
                '//*[@id="settings"]/tbody/tr[17]/td[2]/div/div/span[3]'
                ).click()

        # scroll to the bottom to save
        drv.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            drv.find_element_by_xpath(
                '//*[@id="settings"]/tbody/tr[51]/td[2]/input').click()
        except NoSuchElementException:
            # new version has changed the layout slightly
            drv.find_element_by_xpath(
                '//*[@id="settings"]/tbody/tr[52]/td[2]/input').click()

        # force it to refresh.
        for _ in range(0, 2):
            drv.get(get_args['settings_api_url'])
        drv.find_element_by_xpath('//*[@id="content"]/button').click()

        drv.find_element_by_name('app_id').send_keys(get_args['app_name'])
        sel = Select(drv.find_element_by_name('app_permissions'))
        sel.select_by_visible_text('Read / Write / Admin')
        sel = Select(drv.find_element_by_name('app_security'))
        sel.select_by_visible_text('none')
        try:
            drv.find_element_by_xpath('//*[@id="apiEditSubmit"]').click()
        except NoSuchElementException:
            # new version has changed the layout slightly
            drv.find_element_by_xpath(
                '//*[@id="popup"]/div[3]/div[1]/button[2]').click()
