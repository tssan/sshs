# SSH Select

This is simple tool to keep all hosts used for ssh connection in one place and have quick access to them.

Functions:

- connect to last used host
- show list of added hosts
- connect to selected host via ssh
- add host (alias, ip/host, user)

## Requirements

* Python3.5+
* pip3


## Install develop option (safe)

1. create python env: `make env-setup`

2. install sshs in created env: `make dev-install`

3. `make dev-sshs`

## Install (at own risk ;p)

1. clone this repo

2. run `make install` (user must have permissions to install packages)


## Uninstall

This is tricky ;p

`make uninstall` (also requires permissions)

After that binary file is still in `/usr/local/bin/`  (debian) so you may want to remove it manually
