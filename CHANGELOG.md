

## v0.1.1

- The setup.py now specifies an executable for this package, so after installing, `phpipam-pyclient` executable will be available in your PATH.
- `PHPIPAM_PYCLIENT_CFG_FILE` environment variable can be used to allow users to specify where the configuration file resides dynamically. It takes higher precedence than the `config.json` file that resides in the application directory.
- The `PHPIpamClient` class now allows optional variables to either auto load the configuration file and open the TCP connection. If you set these flags to false you're expected to call `self.load_config()` and `self.auth_session()`.

### New commands

```
phpipam-pyclient version
```
