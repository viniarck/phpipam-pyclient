Configuration
=============

In order to connect to PHPIpam REST API you have to edit the ``phpipam_pyclient/config.json`` file, which by default comes with the following configuration:

::

  {
  "base_url":"http://ipam/api",
  "api_name":"testing",
  "user":"admin",
  "passwd":"my-secret-pw"
  }


- ``base_url``: This is the url of PHPIpam API ``http(s)://<phpipam_server>/api``, make sure to adjust either http or https and the hostname of the PHPIpam server accordingly.
- ``api_name``: The name of the API you have enabled on PHPIpam settings.
- ``user``: username that will be authenticated on PHPIpam
- ``passwd``: user's password

Optionally, if you don't want to specify another location for the `config.json` file, you can set the environment variable `PHPIPAM_PYCLIENT_CFG_FILE` which has higher precedence.

.. note::

  When you enable API either choose ssl if you have https enabled or leave it as None for http. I haven't tested the crypto option.
