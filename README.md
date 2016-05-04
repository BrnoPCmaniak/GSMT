GSMT - Game Server Managment Tool
=================================

GSMT is perfect tool to keep your game server under control.

Features
--------
* Multiple servers
* united starter

Tutorial
--------

1. In `/etc/GSMT` create config file for game server:
2. The file should look like this:
```
[main]
type = minecraft_vanila
path = /opt/mc_server
# start server on daemon start
start_on_daemon_start = True
# with java <options>
java_options = -Xms1024M -Xmx2048M
# name of Jar file
jar_file = minecraft_server.1.9.2.jar
```

* **Name** - Name of server is defined in section header (e.g. `[main]`)
* **type** - Type of server. Choose type from `GSMT/servers_library`.
* **path** - Path to the root folder of game server.
* **start_on_daemon_start** - Wheather the game server should automaticly start with daemon

_others are game server specific options_

Executables
-----------

### gsmt-daemon


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

game_servers
------------

### minecraft_vanila
Server for vanila game server from Mojang.

Specifics:

* **java_options** - Options for Java when running.
* **jar_file** - Options to select mincraft.jar file.


TODO
----

* Implement HTTPS for xmlrpc
* Implement authentication
* User client
* xmlrpc dispatch
* tests
* update game server config
