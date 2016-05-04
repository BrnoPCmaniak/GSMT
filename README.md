===========
GSMT - Game Server Managment Tool
===========

GSMT is perfect tool to keep your game server under control.

Executables
===========

gsmt-daemon
-----------

```
usage: gsmt-daemon [-h] [-v] [-f] [-c CONFIG] [-p PATH] [-s SERVERS_PATH]
                   [-P PORT] [-a ADRESS] [-u USER] [-g GROUP]

GSMT - Game Server Managment Tool Useful tool for server managment. Args that
start with '--' (eg. -v) can also be set in a config file (/etc/GSMT/gsmt.ini
or ./gsmt.ini or specified via -c). The recognized syntax for setting (key,
value) pairs is based on the INI and YAML formats (e.g. key=value or
foo=TRUE). For full documentation of the differences from the standards please
refer to the ConfigArgParse documentation. If an arg is specified in more than
one place, then commandline values override config file values which override
defaults.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Log debug messages.
  -f, --foreground      Do not fork stay in foregroud.
  -c CONFIG, --config CONFIG
                        path to the config file
  -p PATH, --path PATH  Path to configs directory.
  -s SERVERS_PATH, --servers-path SERVERS_PATH
                        Path to servers location.
  -P PORT, --port PORT  Port for GSMT server.
  -a ADRESS, --adress ADRESS
                        Adress for GSMT server.
  -u USER, --user USER  User under who to run the daemon.
  -g GROUP, --group GROUP
                        Group under who to run the daemon.
```
