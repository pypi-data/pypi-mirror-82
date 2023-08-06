# sbsecuretunnel

A python module to make using tunnels easy.

Note: this is pre-release software. If you encounter any problems,
please reach out to CrossBrowserTesting

## pip

`pip install sbsecuretunnel`

## How to use

```
from sbsecuretunnel.sb_securetunnel import SBTunnel
tunnel = SBTunnel(username="you@email.com", authkey="yourauthkey")
tunnel.start_tunnel()
...
tunnel.kill_tunnel()
```

## Features

- Automatically gets the correct tunnel for your platform
- Handles cleanly starting and stopping the tunnel connection
- Handles all features of the tunnel

## Creating a tunnel object

The tunnel object is created with the following options:

- `username` ("") - CBT username
- `authkey` ("") - CBT authkey
- `delete_after` (False) - delete the tunnel binary after kill (note: on Windows, make sure backslashes are escaped `\\`)
- `tunnel_location` (".") - location to download tunnel binary to
- `ready_file` ("ready.check") - ready file for tunnel client
- `kill_file` ("kill.check") - kill file for tunnel client

## Tunnel options

These are all methods available on the tunnel object

- `bypass(bool)` - enable or disable bypass
- `set_https_proxy(string)` - string should be the HTTPS proxy
- `set_http_proxy(string)` - same as above for HTTP
- `set_tunnel_name(string)` - set the name of the named tunnel
- `set_pac_file(string)` - set the client to use the PAC file at path string
- `set_html_path(string)` - set the path to use for local HTML files to be served
- `set_proxy(host="string", port="string", username="string"/None, password="string/None)` - set proxy settings
- `set_accept_all_certs(bool)` - set whether to accept all certs in the tunnel client
